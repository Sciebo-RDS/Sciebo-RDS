{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "layer0_describo.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "layer0_describo.fullname" -}}
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
{{- define "layer0_describo.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Return the proper describo image name
*/}}
{{- define "image" -}}
{{- $registryName := .imageRoot.registry -}}
{{- $repositoryName := .imageRoot.repository -}}
{{- if .repository -}}
{{- $repositoryName = .repository -}}
{{- end -}}
{{- $tag := .imageRoot.tag | toString -}}
{{- if .global }}
    {{- if .global.image }}
        {{- if .global.image.registry }}    
            {{- $registryName = .global.image.registry -}}
        {{- end -}}
    {{- end -}}
{{- end -}}
{{- if $registryName }}
{{- printf "%s/%s:%s" $registryName $repositoryName $tag -}}
{{- else -}}
{{- printf "%s:%s" $repositoryName $tag -}}
{{- end -}}
{{- end -}}

{{/*
Return the proper describo image name
*/}}
{{- define "layer0_describo.apiImage" -}}
{{- include "image" (dict "imageRoot" .Values.image "global" .Values.global "repository" .Values.image.apiRepository) -}}
{{- end -}}

{{- define "layer0_describo.uiImage" -}}
{{ include "image" (dict "imageRoot" .Values.image "global" .Values.global "repository" .Values.image.uiRepository ) }}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "layer0_describo.labels" -}}
app.kubernetes.io/name: {{ include "layer0_describo.name" . }}
helm.sh/chart: {{ include "layer0_describo.chart" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- if .Values.labels }}
{{ toYaml .Values.labels }}
{{- end -}}
{{- end -}}

{{- define "layer0_describo.domain" -}}
{{- if .Values.global }}
{{- .Values.global.domain }}
{{- else if hasKey .Values "domain" }}
{{- .Values.domain  }}
{{- else }}localhost{{- end -}}
{{- end -}}
