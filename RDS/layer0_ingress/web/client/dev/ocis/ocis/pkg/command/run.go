package command

import (
	"fmt"
	"log"
	"net"
	"net/rpc"
	"os"

	cli "github.com/micro/cli/v2"

	"github.com/owncloud/ocis/ocis-pkg/config"
	"github.com/owncloud/ocis/ocis/pkg/register"
)

// RunCommand is the entrypoint for the run command.
func RunCommand(cfg *config.Config) *cli.Command {
	return &cli.Command{
		Name:     "run",
		Usage:    "Runs an extension",
		Category: "Runtime",
		Flags: []cli.Flag{
			&cli.StringFlag{
				Name:        "hostname",
				Value:       "localhost",
				EnvVars:     []string{"OCIS_RUNTIME_HOST"},
				Destination: &cfg.Runtime.Host,
			},
			&cli.StringFlag{
				Name:        "port",
				Value:       "9250",
				EnvVars:     []string{"OCIS_RUNTIME_PORT"},
				Destination: &cfg.Runtime.Port,
			},
		},
		Action: func(c *cli.Context) error {
			client, err := rpc.DialHTTP("tcp", net.JoinHostPort(cfg.Runtime.Host, cfg.Runtime.Port))
			if err != nil {
				log.Fatal("dialing:", err)
			}

			var reply int

			if err := client.Call("Service.Start", os.Args[2], &reply); err != nil {
				log.Fatal(err)
			}
			fmt.Println(reply)

			return nil
		},
	}
}

func init() {
	register.AddCommand(RunCommand)
}
