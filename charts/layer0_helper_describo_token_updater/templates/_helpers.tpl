{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "layer0_helper_describo_token_updater.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "layer0_helper_describo_token_updater.image" -}}
{{ include "common.image" (dict "imageRoot" .Values.image "global" .Values.global) }}
{{- end -}}


{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "layer0_helper_describo_token_updater.fullname" -}}
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
{{- define "layer0_helper_describo_token_updater.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "layer0_helper_describo_token_updater.labels" -}}
app.kubernetes.io/name: {{ include "layer0_helper_describo_token_updater.name" . }}
helm.sh/chart: {{ include "layer0_helper_describo_token_updater.chart" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- if .Values.labels }}
{{ toYaml .Values.labels }}
{{- end -}}
{{- end -}}


{{- define "layer0_helper_describo_token_updater.domain" -}}
{{- if .Values.global }}
{{- .Values.global.domain -}}
{{- else if hasKey .Values "domain" }}
{{- .Values.domain -}}
{{- else }}"localhost"{{- end -}}
{{- end -}}

{{- define "layer0_helper_describo_token_updater.secretName" -}}
{{- if .Values.global}}
{{ .Values.global.ingress.tls.secretName }}
{{- else }}
{{ .Values.ingress.tls.secretName }}
{{- end -}}
{{- end -}}