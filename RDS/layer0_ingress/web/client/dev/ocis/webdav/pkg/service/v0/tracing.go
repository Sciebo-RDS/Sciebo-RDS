package svc

import (
	"net/http"
)

// NewTracing returns a service that instruments traces.
func NewTracing(next Service) Service {
	return tracing{
		next: next,
	}
}

type tracing struct {
	next Service
}

// ServeHTTP implements the Service interface.
func (t tracing) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	t.next.ServeHTTP(w, r)
}

// Thumbnail implements the Service interface.
func (t tracing) Thumbnail(w http.ResponseWriter, r *http.Request) {
	t.next.Thumbnail(w, r)
}
