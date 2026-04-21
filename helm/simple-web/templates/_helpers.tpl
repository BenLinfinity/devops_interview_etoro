{{/*
Create the instance label to allow labeling items according to chart
*/}}
{{- define "simple-web.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create the instance name to allow labeling items according to release
*/}}
{{- define "simple-web.instance" -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Used for naming items with chart and release name
*/}}
{{- define "simple-web.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
used to label items with tags by chart, release, management tool
*/}}
{{- define "simple-web.labels" -}}
app.kubernetes.io/name: {{ include "simple-web.name" . }}
app.kubernetes.io/instance: {{ include "simple-web.instance" .}}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Create the name for the image pull secret
*/}}
{{- define "simple-web.imagePullSecretName" -}}
{{- $base := include "simple-web.fullname" . -}}
{{- printf "%s-%s" $base "image-pull-secret" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create the name for the KEDA scaled object
*/}}
{{- define "simple-web.scaledObjectName" -}}
{{- $base := include "simple-web.fullname" . -}}
{{- printf "%s-%s" $base "autoscaler" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create the name for ingress rules
*/}}
{{- define "simple-web.ingressRuleName" -}}
{{- $base := include "simple-web.fullname" . -}}
{{- printf "%s-%s" $base "ingress" | trunc 63 | trimSuffix "-" -}}
{{- end -}}