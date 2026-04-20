{{- define "simple-web.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "simple-web.labels" -}}
app.kubernetes.io/name: {{ include "simple-web.name" . }}
{{- end -}}
