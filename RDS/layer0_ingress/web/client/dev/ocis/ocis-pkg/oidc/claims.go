package oidc

// The ProviderMetadata describes an idp.
// see https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderMetadata
type ProviderMetadata struct {
	AuthorizationEndpoint string `json:"authorization_endpoint,omitempty"`
	//claims_parameter_supported
	ClaimsSupported []string `json:"claims_supported,omitempty"`
	//grant_types_supported
	IDTokenSigningAlgValuesSupported []string `json:"id_token_signing_alg_values_supported,omitempty"`
	Issuer                           string   `json:"issuer,omitempty"`
	JwksURI                          string   `json:"jwks_uri,omitempty"`
	//registration_endpoint
	//request_object_signing_alg_values_supported
	//request_parameter_supported
	//request_uri_parameter_supported
	//require_request_uri_registration
	//response_modes_supported
	ResponseTypesSupported []string `json:"response_types_supported,omitempty"`
	ScopesSupported        []string `json:"scopes_supported,omitempty"`
	SubjectTypesSupported  []string `json:"subject_types_supported,omitempty"`
	TokenEndpoint          string   `json:"token_endpoint,omitempty"`
	//token_endpoint_auth_methods_supported
	//token_endpoint_auth_signing_alg_values_supported
	UserinfoEndpoint string `json:"userinfo_endpoint,omitempty"`
	//userinfo_signing_alg_values_supported
	//code_challenge_methods_supported
	IntrospectionEndpoint string `json:"introspection_endpoint,omitempty"`
	//introspection_endpoint_auth_methods_supported
	//introspection_endpoint_auth_signing_alg_values_supported
	RevocationEndpoint string `json:"revocation_endpoint,omitempty"`
	//revocation_endpoint_auth_methods_supported
	//revocation_endpoint_auth_signing_alg_values_supported
	//id_token_encryption_alg_values_supported
	//id_token_encryption_enc_values_supported
	//userinfo_encryption_alg_values_supported
	//userinfo_encryption_enc_values_supported
	//request_object_encryption_alg_values_supported
	//request_object_encryption_enc_values_supported
	CheckSessionIframe string `json:"check_session_iframe,omitempty"`
	EndSessionEndpoint string `json:"end_session_endpoint,omitempty"`
	//claim_types_supported
}

// StandardClaims will be stored in the context to be consumed by the oidc user manager
// They can be requested to be returned either in the UserInfo Response, per
// Section 5.3.2, or in the ID Token, per Section 2.
// see https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims
type StandardClaims struct {
	// Time the End-User's information was last updated. Its value is a
	// JSON number representing the number of seconds from 1970-01-01T0:0:0Z
	// as measured in UTC until the date/time.
	UpdatedAt int64 `json:"updated_at,omitempty"`

	// True if the End-User's e-mail address has been verified; otherwise false.
	// When this Claim Value is true, this means that the OP took affirmative
	// steps to ensure that this e-mail address was controlled by the End-User
	// at the time the verification was performed. The means by which an e-mail
	// address is verified is context-specific, and dependent upon the trust
	// framework or contractual agreements within which the parties are operating.
	EmailVerified bool `json:"email_verified,omitempty"`

	// True if the End-User's phone number has been verified; otherwise false.
	// When this Claim Value is true, this means that the OP took affirmative
	// steps to ensure that this phone number was controlled by the End-User
	// at the time the verification was performed. The means by which a phone
	// number is verified is context-specific, and dependent upon the trust
	// framework or contractual agreements within which the parties are
	// operating. When true, the phone_number Claim MUST be in E.164 format
	// and any extensions MUST be represented in RFC 3966 format.
	PhoneNumberVerified bool `json:"phone_number_verified,omitempty"`

	Iss string `json:"iss"`

	// Subject - Identifier for the End-User at the Issuer.
	Sub string `json:"sub,omitempty"`

	// End-User's full name in displayable form including all name parts, possibly
	// including titles and suffixes, ordered according to the End-User's locale
	// and preferences.
	Name string `json:"name,omitempty"`

	// Given name(s) or first name(s) of the End-User. Note that in some cultures,
	// people can have multiple given names; all can be present, with the names
	// being separated by space characters.
	GivenName string `json:"given_name,omitempty"`

	// Surname(s) or last name(s) of the End-User. Note that in some cultures,
	// people can have multiple family names or no family name; all can be present,
	// with the names being separated by space characters.
	FamilyName string `json:"family_name,omitempty"`

	// Middle name(s) of the End-User. Note that in some cultures, people can have
	// multiple middle names; all can be present, with the names being separated by
	// space characters. Also note that in some cultures, middle names are not used.
	MiddleName string `json:"middle_name,omitempty"`

	// Casual name of the End-User that may or may not be the same as the given_name.
	// For instance, a nickname value of Mike might be returned alongside a given_name
	// value of Michael.
	Nickname string `json:"nickname,omitempty"`

	// Shorthand name by which the End-User wishes to be referred to at the RP, such
	// as janedoe or j.doe. This value MAY be any valid JSON string including special
	// characters such as @, /, or whitespace. The RP MUST NOT rely upon this value
	// being unique, as discussed in Section 5.7.
	PreferredUsername string `json:"preferred_username,omitempty"`

	// URL of the End-User's profile page. The contents of this Web page SHOULD be
	// about the End-User.
	Profile string `json:"profile,omitempty"`

	// URL of the End-User's profile picture. This URL MUST refer to an image file
	// (for example, a PNG, JPEG, or GIF image file), rather than to a Web page
	// containing an image. Note that this URL SHOULD specifically reference a
	// profile photo of the End-User suitable for displaying when describing the
	// End-User, rather than an arbitrary photo taken by the End-User.
	Picture string `json:"picture,omitempty"`

	// URL of the End-User's Web page or blog. This Web page SHOULD contain
	// information published by the End-User or an organization that the End-User
	// is affiliated with.
	Website string `json:"website,omitempty"`

	// End-User's preferred e-mail address. Its value MUST conform to the RFC 5322
	// addr-spec syntax. The RP MUST NOT rely upon this value being unique, as
	// discussed in Section 5.7.
	Email string `json:"email,omitempty"`

	// End-User's gender. Values defined by this specification are female and male.
	// Other values MAY be used when neither of the defined values are applicable.
	Gender string `json:"gender,omitempty"`

	// End-User's birthday, represented as an ISO 8601:2004 YYYY-MM-DD format.
	// The year MAY be 0000, indicating that it is omitted. To represent only the
	// year, YYYY format is allowed. Note that depending on the underlying
	// platform's date related function, providing just year can result in
	// varying month and day, so the implementers need to take this factor into
	// account to correctly process the dates.
	Birthdate string `json:"birthdate,omitempty"`

	// String from zoneinfo time zone database representing the End-User's time
	// zone. For example, Europe/Paris or America/Los_Angeles.
	Zoneinfo string `json:"zoneinfo,omitempty"`

	// End-User's locale, represented as a BCP47 [RFC5646] language tag.
	// This is typically an ISO 639-1 Alpha-2 [ISO639‑1] language code in
	// lowercase and an ISO 3166-1 Alpha-2 [ISO3166‑1] country code in
	// uppercase, separated by a dash. For example, en-US or fr-CA. As a
	// compatibility note, some implementations have used an underscore as
	// the separator rather than a dash, for example, en_US; Relying Parties
	// MAY choose to accept this locale syntax as well.
	Locale string `json:"locale,omitempty"`

	// End-User's preferred telephone number. E.164 [E.164] is RECOMMENDED
	// as the format of this Claim, for example, +1 (425) 555-1212 or
	// +56 (2) 687 2400. If the phone number contains an extension, it is
	// RECOMMENDED that the extension be represented using the RFC 3966
	// extension syntax, for example, +1 (604) 555-1234;ext=5678.
	PhoneNumber string `json:"phone_number,omitempty"`

	// TODO Name is the correct one, does kopano use display name? -> double check and report bug
	DisplayName string `json:"display_name,omitempty"`

	Groups []string `json:"groups,omitempty"`

	// End-User's preferred postal address. The value of the address member
	// is a JSON [RFC4627] structure containing some or all of the members
	// defined in Section 5.1.1.
	// TODO add address claim https://openid.net/specs/openid-connect-core-1_0.html#AddressClaim
	Address    map[string]interface{} `json:"address,omitempty"`
	KCIdentity map[string]string      `json:"kc.identity,omitempty"`

	// To integrate with an existing LDAP server the IdP can send the numeric user and group id:

	// UIDNumber is a unique numerical id that will be used when setting acls on a storage that integrates with the OS/LDAP
	UIDNumber string `json:"uidnumber,omitempty"`
	// GIDNumber is a unique numerical id that will be used when setting acls on a storage that integrates with the OS/LDAP
	GIDNumber string `json:"gidnumber,omitempty"`

	// OcisID is a unique, persistent, non reassignable user id
	OcisID string `json:"ocis.id,omitempty"`
}
