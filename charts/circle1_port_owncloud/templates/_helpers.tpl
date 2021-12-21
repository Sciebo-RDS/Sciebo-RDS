{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "circle1_port_owncloud.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "circle1_port_owncloud.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "circle1_port_owncloud.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "circle1_port_owncloud.labels" -}}
app.kubernetes.io/name: {{ include "circle1_port_owncloud.name" . }}
helm.sh/chart: {{ include "circle1_port_owncloud.chart" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- if .Values.labels }}
{{ toYaml .Values.labels }}
{{- end -}}
{{- end -}}

{{- define "circle1_port_owncloud.domain" -}}
{{- if .Values.global }}
{{- .Values.global.domain -}}
{{- else if hasKey .Values "domain" }}
{{- .Values.domain -}}
{{- else }}"localhost"{{- end -}}
{{- end -}}

{{- define "circle1_port_owncloud.secretName" -}}
{{- if .Values.global}}
{{ .Values.global.ingress.tls.secretName }}
{{- else }}
{{ .Values.ingress.tls.secretName }}
{{- end -}}
{{- end -}}