package command

import (
	"context"
	"strings"

	glauthcfg "github.com/glauth/glauth/pkg/config"
	"github.com/micro/cli/v2"
	"github.com/oklog/run"
	accounts "github.com/owncloud/ocis/accounts/pkg/proto/v0"
	"github.com/owncloud/ocis/glauth/pkg/config"
	"github.com/owncloud/ocis/glauth/pkg/flagset"
	"github.com/owncloud/ocis/glauth/pkg/metrics"
	"github.com/owncloud/ocis/glauth/pkg/server/debug"
	"github.com/owncloud/ocis/glauth/pkg/server/glauth"
	"github.com/owncloud/ocis/glauth/pkg/tracing"
	pkgcrypto "github.com/owncloud/ocis/ocis-pkg/crypto"
	"github.com/owncloud/ocis/ocis-pkg/service/grpc"
	"github.com/owncloud/ocis/ocis-pkg/sync"
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
			cfg.Backend.Servers = ctx.StringSlice("backend-server")
			cfg.Fallback.Servers = ctx.StringSlice("fallback-server")
			if !cfg.Supervised {
				return ParseConfig(ctx, cfg)
			}
			logger.Debug().Str("service", "glauth").Msg("ignoring config file parsing when running supervised")
			return nil
		},
		Action: func(c *cli.Context) error {
			logger := NewLogger(cfg)

			if err := tracing.Configure(cfg, logger); err != nil {
				return err
			}

			gr := run.Group{}
			ctx, cancel := func() (context.Context, context.CancelFunc) {
				if cfg.Context == nil {
					return context.WithCancel(context.Background())
				}
				return context.WithCancel(cfg.Context)
			}()
			metrics := metrics.New()

			defer cancel()

			metrics.BuildInfo.WithLabelValues(cfg.Version).Set(1)

			{

				lcfg := glauthcfg.LDAP{
					Enabled: cfg.Ldap.Enabled,
					Listen:  cfg.Ldap.Address,
				}
				lscfg := glauthcfg.LDAPS{
					Enabled: cfg.Ldaps.Enabled,
					Listen:  cfg.Ldaps.Address,
					Cert:    cfg.Ldaps.Cert,
					Key:     cfg.Ldaps.Key,
				}
				bcfg := glauthcfg.Config{
					LDAP:  lcfg,  // TODO remove LDAP from the backend config upstream
					LDAPS: lscfg, // TODO remove LDAP from the backend config upstream
					Backend: glauthcfg.Backend{
						Datastore:   cfg.Backend.Datastore,
						BaseDN:      cfg.Backend.BaseDN,
						Insecure:    cfg.Backend.Insecure,
						NameFormat:  cfg.Backend.NameFormat,
						GroupFormat: cfg.Backend.GroupFormat,
						Servers:     cfg.Backend.Servers,
						SSHKeyAttr:  cfg.Backend.SSHKeyAttr,
						UseGraphAPI: cfg.Backend.UseGraphAPI,
					},
				}
				fcfg := glauthcfg.Config{
					LDAP:  lcfg,  // TODO remove LDAP from the backend config upstream
					LDAPS: lscfg, // TODO remove LDAP from the backend config upstream
					Backend: glauthcfg.Backend{
						Datastore:   cfg.Fallback.Datastore,
						BaseDN:      cfg.Fallback.BaseDN,
						Insecure:    cfg.Fallback.Insecure,
						NameFormat:  cfg.Fallback.NameFormat,
						GroupFormat: cfg.Fallback.GroupFormat,
						Servers:     cfg.Fallback.Servers,
						SSHKeyAttr:  cfg.Fallback.SSHKeyAttr,
						UseGraphAPI: cfg.Fallback.UseGraphAPI,
					},
				}

				if lscfg.Enabled {
					if err := pkgcrypto.GenCert(cfg.Ldaps.Cert, cfg.Ldaps.Key, logger); err != nil {
						logger.Fatal().Err(err).Msgf("Could not generate test-certificate")
					}
				}

				as, gs := getAccountsServices()
				server, err := glauth.Server(
					glauth.AccountsService(as),
					glauth.GroupsService(gs),
					glauth.Logger(logger),
					glauth.LDAP(&lcfg),
					glauth.LDAPS(&lscfg),
					glauth.Backend(&bcfg),
					glauth.Fallback(&fcfg),
					glauth.RoleBundleUUID(cfg.RoleBundleUUID),
				)

				if err != nil {
					logger.Info().
						Err(err).
						Str("transport", "ldap").
						Msg("Failed to initialize server")

					return err
				}

				gr.Add(func() error {
					err := make(chan error)
					select {
					case <-ctx.Done():
						return nil
					case err <- server.ListenAndServe():
						return <-err
					}

				}, func(_ error) {
					logger.Info().
						Str("transport", "ldap").
						Msg("Shutting down server")

					server.Shutdown()
					cancel()
				})

				gr.Add(func() error {
					err := make(chan error)
					select {
					case <-ctx.Done():
						return nil
					case err <- server.ListenAndServeTLS():
						return <-err
					}

				}, func(_ error) {
					logger.Info().
						Str("transport", "ldaps").
						Msg("Shutting down server")

					server.Shutdown()
					cancel()
				})

			}

			{
				server, err := debug.Server(
					debug.Logger(logger),
					debug.Context(ctx),
					debug.Config(cfg),
				)

				if err != nil {
					logger.Info().Err(err).Str("transport", "debug").Msg("Failed to initialize server")
					return err
				}

				gr.Add(server.ListenAndServe, func(_ error) {
					_ = server.Shutdown(ctx)
					cancel()
				})
			}

			if !cfg.Supervised {
				sync.Trap(&gr, cancel)
			}

			return gr.Run()
		},
	}
}

// getAccountsServices returns an ocis-accounts service
func getAccountsServices() (accounts.AccountsService, accounts.GroupsService) {
	return accounts.NewAccountsService("com.owncloud.api.accounts", grpc.DefaultClient),
		accounts.NewGroupsService("com.owncloud.api.accounts", grpc.DefaultClient)
}
