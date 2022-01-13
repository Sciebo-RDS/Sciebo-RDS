{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "layer1_port_openscienceframework.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "layer1_port_openscienceframework.image" -}}
{{ include "common.image" (dict "imageRoot" .Values.image "global" .Values.global) }}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "layer1_port_openscienceframework.fullname" -}}
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
{{- define "layer1_port_openscienceframework.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "layer1_port_openscienceframework.labels" -}}
app.kubernetes.io/name: {{ include "layer1_port_openscienceframework.name" . }}
helm.sh/chart: {{ include "layer1_port_openscienceframework.chart" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- if .Values.labels }}
{{ toYaml .Values.labels }}
{{- end -}}
{{- end -}}


{{- define "layer1_port_openscienceframework.domain" -}}
{{- if .Values.global }}
{{- .Values.global.domain -}}
{{- else if hasKey .Values "domain" }}
{{- .Values.domain -}}
{{- else }}"localhost"{{- end -}}
{{- end -}}

{{- define "layer1_port_openscienceframework.secretName" -}}
{{- if .Values.global}}
{{ .Values.global.ingress.tls.secretName }}
{{- else }}
{{ .Values.ingress.tls.secretName }}
{{- end -}}
{{- end -}}