package command

import (
	"context"
	"strings"

	"github.com/micro/cli/v2"
	"github.com/oklog/run"
	"github.com/owncloud/ocis/ocis-pkg/sync"
	"github.com/owncloud/ocis/settings/pkg/config"
	"github.com/owncloud/ocis/settings/pkg/flagset"
	"github.com/owncloud/ocis/settings/pkg/metrics"
	"github.com/owncloud/ocis/settings/pkg/server/debug"
	"github.com/owncloud/ocis/settings/pkg/server/grpc"
	"github.com/owncloud/ocis/settings/pkg/server/http"
	"github.com/owncloud/ocis/settings/pkg/tracing"
)

// Server is the entrypoint for the server command.
func Server(cfg *config.Config) *cli.Command {
	return &cli.Command{
		Name:  "server",
		Usage: "Start integrated server",
		Flags: flagset.ServerWithConfig(cfg),
		Before: func(ctx *cli.Context) error {
			logger := NewLogger(cfg)
			if cfg.HTTP.Root != "/" {
				cfg.HTTP.Root = strings.TrimSuffix(cfg.HTTP.Root, "/")
			}

			// When running on single binary mode the before hook from the root command won't get called. We manually
			// call this before hook from ocis command, so the configuration can be loaded.
			if !cfg.Supervised {
				return ParseConfig(ctx, cfg)
			}
			logger.Debug().Str("service", "settings").Msg("ignoring config file parsing when running supervised")
			return nil
		},
		Action: func(c *cli.Context) error {
			logger := NewLogger(cfg)

			err := tracing.Configure(cfg, logger)
			if err != nil {
				return err
			}

			servers := run.Group{}
			ctx, cancel := func() (context.Context, context.CancelFunc) {
				if cfg.Context == nil {
					return context.WithCancel(context.Background())
				}
				return context.WithCancel(cfg.Context)
			}()
			defer cancel()

			mtrcs := metrics.New()
			mtrcs.BuildInfo.WithLabelValues(cfg.Service.Version).Set(1)

			// prepare an HTTP server and add it to the group run.
			httpServer := http.Server(
				http.Name(cfg.Service.Name),
				http.Logger(logger),
				http.Context(ctx),
				http.Config(cfg),
				http.Metrics(mtrcs),
			)
			servers.Add(httpServer.Run, func(_ error) {
				logger.Info().Str("server", "http").Msg("Shutting down server")
				cancel()
			})

			// prepare a gRPC server and add it to the group run.
			grpcServer := grpc.Server(grpc.Name(cfg.Service.Name), grpc.Logger(logger), grpc.Context(ctx), grpc.Config(cfg), grpc.Metrics(mtrcs))
			servers.Add(grpcServer.Run, func(_ error) {
				logger.Info().Str("server", "grpc").Msg("Shutting down server")
				cancel()
			})

			// prepare a debug server and add it to the group run.
			debugServer, err := debug.Server(debug.Logger(logger), debug.Context(ctx), debug.Config(cfg))
			if err != nil {
				logger.Error().Err(err).Str("server", "debug").Msg("Failed to initialize server")
				return err
			}

			servers.Add(debugServer.ListenAndServe, func(_ error) {
				_ = debugServer.Shutdown(ctx)
				cancel()
			})

			if !cfg.Supervised {
				sync.Trap(&servers, cancel)
			}

			return servers.Run()
		},
	}
}
