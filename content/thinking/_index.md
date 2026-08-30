---
title: "开源之思"
slug: "thinking"
date: 2026-08-28
type: thinking
cover: "thinking-cover.jpeg"
author: "适兕"
description: "适兕的思想札记——制度经济学、文化批判与政治经济学的碎片化观察，21 篇"
work_type: 7
---

<div class="book-hero">
  <div class="book-hero-cover">
    <img src="/thinking-cover.jpeg" alt="开源之思 封面">
  </div>
  <div class="book-hero-text">
    <h1>开源之思</h1>
    <div class="hero-meta">
      <span>「开源之道」· 适兕</span>
      <span>·</span>
      <span>21 篇思想札记</span>
    </div>
    <p class="hero-desc">思想札记系列——制度经济学、文化批判与政治经济学的碎片化观察。从 The Bitter Lesson 到 Habermas 的公共领域，从 GNU 的 copyleft 制度内化到「机构使人麻木」，21 篇札记围绕一个核心问题：开源作为制度契约，如何在西方语境中被理解，又为何在中国本土被置换为另一套逻辑？</p>
    <div class="hero-cta">
      <a href="#list" class="btn-primary">阅读札记</a>
      <a href="https://www.opensourceway.blog/" class="btn-ghost" target="_blank" rel="noopener">更多思想长文 ↗</a>
    </div>
    <p class="hero-note">仅在线阅读，不提供 PDF/EPUB 下载。</p>
  </div>
</div>

<h2 id="list" class="thinking-list-header">思想札记列表</h2>
<div class="thinking-list">
  {{ range .Pages.ByDate.Reverse }}
  <a href="{{ .RelPermalink }}" class="thinking-card">
    <div class="thinking-card-date">{{ .Date.Format "2006-01-02" }}</div>
    <div class="thinking-card-body">
      <h3>{{ .Title }}</h3>
      {{ if .Description }}<p>{{ .Description }}</p>{{ end }}
    </div>
  </a>
  {{ end }}
</div>
