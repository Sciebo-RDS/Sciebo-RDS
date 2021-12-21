package middleware

import (
	"github.com/owncloud/ocis/proxy/pkg/user/backend"
	"net/http"
	"time"

	settings "github.com/owncloud/ocis/settings/pkg/proto/v0"

	gateway "github.com/cs3org/go-cs3apis/cs3/gateway/v1beta1"
	acc "github.com/owncloud/ocis/accounts/pkg/proto/v0"
	"github.com/owncloud/ocis/ocis-pkg/log"
	"github.com/owncloud/ocis/proxy/pkg/config"
	storepb "github.com/owncloud/ocis/store/pkg/proto/v0"
)

// Option defines a single option function.
type Option func(o *Options)

// Options defines the available options for this package.
type Options struct {
	// Logger to use for logging, must be set
	Logger log.Logger
	// TokenManagerConfig for communicating with the reva token manager
	TokenManagerConfig config.TokenManager
	// HTTPClient to use for communication with the oidcAuth provider
	HTTPClient *http.Client
	// AccountsClient for resolving accounts
	AccountsClient acc.AccountsService
	// UP
	UserProvider backend.UserBackend
	// SettingsRoleService for the roles API in settings
	SettingsRoleService settings.RoleService
	// OIDCProviderFunc to lazily initialize an oidc provider, must be set for the oidc_auth middleware
	OIDCProviderFunc func() (OIDCProvider, error)
	// OIDCIss is the oidcAuth-issuer
	OIDCIss string
	// RevaGatewayClient to send requests to the reva gateway
	RevaGatewayClient gateway.GatewayAPIClient
	// Store for persisting data
	Store storepb.StoreService
	// PreSignedURLConfig to configure the middleware
	PreSignedURLConfig config.PreSignedURL
	// AutoprovisionAccounts when an accountResolver does not exist.
	AutoprovisionAccounts bool
	// EnableBasicAuth to allow basic auth
	EnableBasicAuth bool
	// UserinfoCacheSize defines the max number of entries in the userinfo cache, intended for the oidc_auth middleware
	UserinfoCacheSize int
	// UserinfoCacheTTL sets the max cache duration for the userinfo cache, intended for the oidc_auth middleware
	UserinfoCacheTTL time.Duration
	// CredentialsByUserAgent sets the auth challenges on a per user-agent basis
	CredentialsByUserAgent map[string]string
}

// newOptions initializes the available default options.
func newOptions(opts ...Option) Options {
	opt := Options{}

	for _, o := range opts {
		o(&opt)
	}

	return opt
}

// Logger provides a function to set the logger option.
func Logger(l log.Logger) Option {
	return func(o *Options) {
		o.Logger = l
	}
}

// TokenManagerConfig provides a function to set the token manger config option.
func TokenManagerConfig(cfg config.TokenManager) Option {
	return func(o *Options) {
		o.TokenManagerConfig = cfg
	}
}

// HTTPClient provides a function to set the http client config option.
func HTTPClient(c *http.Client) Option {
	return func(o *Options) {
		o.HTTPClient = c
	}
}

// AccountsClient provides a function to set the accounts client config option.
func AccountsClient(ac acc.AccountsService) Option {
	return func(o *Options) {
		o.AccountsClient = ac
	}
}

// SettingsRoleService provides a function to set the role service option.
func SettingsRoleService(rc settings.RoleService) Option {
	return func(o *Options) {
		o.SettingsRoleService = rc
	}
}

// OIDCProviderFunc provides a function to set the the oidc provider function option.
func OIDCProviderFunc(f func() (OIDCProvider, error)) Option {
	return func(o *Options) {
		o.OIDCProviderFunc = f
	}
}

// OIDCIss sets the oidcAuth issuer url
func OIDCIss(iss string) Option {
	return func(o *Options) {
		o.OIDCIss = iss
	}
}

// CredentialsByUserAgent sets UserAgentChallenges.
func CredentialsByUserAgent(v map[string]string) Option {
	return func(o *Options) {
		o.CredentialsByUserAgent = v
	}
}

// RevaGatewayClient provides a function to set the the reva gateway service client option.
func RevaGatewayClient(gc gateway.GatewayAPIClient) Option {
	return func(o *Options) {
		o.RevaGatewayClient = gc
	}
}

// Store provides a function to set the store option.
func Store(sc storepb.StoreService) Option {
	return func(o *Options) {
		o.Store = sc
	}
}

// PreSignedURLConfig provides a function to set the PreSignedURL config
func PreSignedURLConfig(cfg config.PreSignedURL) Option {
	return func(o *Options) {
		o.PreSignedURLConfig = cfg
	}
}

// AutoprovisionAccounts provides a function to set the AutoprovisionAccounts config
func AutoprovisionAccounts(val bool) Option {
	return func(o *Options) {
		o.AutoprovisionAccounts = val
	}
}

// EnableBasicAuth provides a function to set the EnableBasicAuth config
func EnableBasicAuth(enableBasicAuth bool) Option {
	return func(o *Options) {
		o.EnableBasicAuth = enableBasicAuth
	}
}

// TokenCacheSize provides a function to set the TokenCacheSize
func TokenCacheSize(size int) Option {
	return func(o *Options) {
		o.UserinfoCacheSize = size
	}
}

// TokenCacheTTL provides a function to set the TokenCacheTTL
func TokenCacheTTL(ttl time.Duration) Option {
	return func(o *Options) {
		o.UserinfoCacheTTL = ttl
	}
}

// UserProvider sets the accounts user provider
func UserProvider(up backend.UserBackend) Option {
	return func(o *Options) {
		o.UserProvider = up
	}
}
