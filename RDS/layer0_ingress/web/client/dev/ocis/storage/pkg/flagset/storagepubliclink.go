package flagset

import (
	"github.com/micro/cli/v2"
	"github.com/owncloud/ocis/ocis-pkg/flags"
	"github.com/owncloud/ocis/storage/pkg/config"
)

// StoragePublicLink applies cfg to the root flagset
func StoragePublicLink(cfg *config.Config) []cli.Flag {
	flags := []cli.Flag{

		&cli.StringFlag{
			Name:        "debug-addr",
			Value:       flags.OverrideDefaultString(cfg.Reva.StoragePublicLink.DebugAddr, "0.0.0.0:9179"),
			Usage:       "Address to bind debug server",
			EnvVars:     []string{"STORAGE_PUBLIC_LINK_DEBUG_ADDR"},
			Destination: &cfg.Reva.StoragePublicLink.DebugAddr,
		},

		&cli.StringFlag{
			Name:        "network",
			Value:       flags.OverrideDefaultString(cfg.Reva.StoragePublicLink.GRPCNetwork, "tcp"),
			Usage:       "Network to use for the storage service, can be 'tcp', 'udp' or 'unix'",
			EnvVars:     []string{"STORAGE_PUBLIC_LINK_GRPC_NETWORK"},
			Destination: &cfg.Reva.StoragePublicLink.GRPCNetwork,
		},
		&cli.StringFlag{
			Name:        "addr",
			Value:       flags.OverrideDefaultString(cfg.Reva.StoragePublicLink.GRPCAddr, "0.0.0.0:9178"),
			Usage:       "Address to bind storage service",
			EnvVars:     []string{"STORAGE_PUBLIC_LINK_GRPC_ADDR"},
			Destination: &cfg.Reva.StoragePublicLink.GRPCAddr,
		},

		&cli.StringFlag{
			Name:        "mount-path",
			Value:       flags.OverrideDefaultString(cfg.Reva.StoragePublicLink.MountPath, "/public"),
			Usage:       "mount path",
			EnvVars:     []string{"STORAGE_PUBLIC_LINK_MOUNT_PATH"},
			Destination: &cfg.Reva.StoragePublicLink.MountPath,
		},

		&cli.StringFlag{
			Name:        "gateway-endpoint",
			Value:       flags.OverrideDefaultString(cfg.Reva.Gateway.Endpoint, "localhost:9142"),
			Usage:       "endpoint to use for the storage gateway service",
			EnvVars:     []string{"STORAGE_GATEWAY_ENDPOINT"},
			Destination: &cfg.Reva.Gateway.Endpoint,
		},
	}

	flags = append(flags, TracingWithConfig(cfg)...)
	flags = append(flags, DebugWithConfig(cfg)...)
	flags = append(flags, SecretWithConfig(cfg)...)

	return flags
}
