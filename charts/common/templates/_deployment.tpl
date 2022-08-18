
{{/*
Return the proper image name
{{ include "common.image" ( dict "imageRoot" .Values.path.to.the.image "global" $) }}
*/}}
{{- define "common.image" -}}
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
        {{- if .global.image.tag -}}
            {{- $tag = .global.image.tag | toString -}}
        {{- end -}}
    {{- end -}}
{{- end -}}
{{- if $registryName }}
{{- printf "%s/%s:%s" $registryName $repositoryName $tag -}}
{{- else -}}
{{- printf "%s:%s" $repositoryName $tag -}}
{{- end -}}
{{- end -}}

{{- define "common.ingressAnnotations" -}}
{{- $annotations := dict -}}
{{- with .Values.ingress.annotations }}
    {{- $annotations = . -}}
{{- end -}}
{{- if .Values.global }}
    {{- if .Values.global.ingress }}
        {{- if .Values.global.ingress.annotations }}
            {{- $annotations = mustMergeOverwrite .Values.global.ingress.annotations $annotations -}}
        {{- end -}}
    {{- end -}}
{{- end -}}
{{- toYaml $annotations -}}
{{- end -}}


{{- define "common.tlsSecretName" -}}
{{- $secretName := "" -}}
{{- if .Values.ingress }}
    {{- if .Values.ingress.tls }}
        {{- if .Values.ingress.tls.secretName }}
            {{- $secretName = .Values.ingress.tls.secretName -}}
        {{- end -}}
    {{- end -}}
{{- end -}}
{{- if .Values.global }}
    {{- if .Values.global.ingress }}
        {{- if .Values.global.ingress.tls }}
            {{- if .Values.global.ingress.tls.secretName }}
                {{- $secretName = .Values.global.ingress.tls.secretName -}}
            {{- end -}}
        {{- end -}}
    {{- end -}}
{{- end -}}
{{- printf "%s" $secretName -}}
{{- end -}}
