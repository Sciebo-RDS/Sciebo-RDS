package middleware

import (
	"net/http"

	gateway "github.com/cs3org/go-cs3apis/cs3/gateway/v1beta1"
	rpc "github.com/cs3org/go-cs3apis/cs3/rpc/v1beta1"
	provider "github.com/cs3org/go-cs3apis/cs3/storage/provider/v1beta1"
	"github.com/cs3org/reva/pkg/rgrpc/status"
	tokenPkg "github.com/cs3org/reva/pkg/token"
	"github.com/cs3org/reva/pkg/token/manager/jwt"
	"github.com/owncloud/ocis/ocis-pkg/log"
	"google.golang.org/grpc/metadata"
)

// CreateHome provides a middleware which sends a CreateHome request to the reva gateway
func CreateHome(optionSetters ...Option) func(next http.Handler) http.Handler {
	options := newOptions(optionSetters...)
	logger := options.Logger

	return func(next http.Handler) http.Handler {
		tokenManager, err := jwt.New(map[string]interface{}{
			"secret": options.TokenManagerConfig.JWTSecret,
		})
		if err != nil {
			logger.Fatal().Err(err).Msgf("Could not initialize token-manager")
		}

		return &createHome{
			next:              next,
			logger:            logger,
			tokenManager:      tokenManager,
			revaGatewayClient: options.RevaGatewayClient,
		}
	}
}

type createHome struct {
	next              http.Handler
	logger            log.Logger
	tokenManager      tokenPkg.Manager
	revaGatewayClient gateway.GatewayAPIClient
}

func (m createHome) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	if !m.shouldServe(req) {
		m.next.ServeHTTP(w, req)
		return
	}

	token := req.Header.Get("x-access-token")

	// we need to pass the token to authenticate the CreateHome request.
	//ctx := tokenpkg.ContextSetToken(r.Context(), token)
	ctx := metadata.AppendToOutgoingContext(req.Context(), tokenPkg.TokenHeader, token)

	createHomeReq := &provider.CreateHomeRequest{}
	createHomeRes, err := m.revaGatewayClient.CreateHome(ctx, createHomeReq)

	if err != nil {
		m.logger.Err(err).Msg("error calling CreateHome")
	} else if createHomeRes.Status.Code != rpc.Code_CODE_OK {
		err := status.NewErrorFromCode(createHomeRes.Status.Code, "gateway")
		m.logger.Err(err).Msg("error when calling Createhome")
	}

	m.next.ServeHTTP(w, req)
}

func (m createHome) shouldServe(req *http.Request) bool {
	return req.Header.Get("x-access-token") != ""
}
