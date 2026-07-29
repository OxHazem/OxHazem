svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 380">
<style>
  @keyframes fadeSlide {
    0%   { opacity: 0; transform: translateY(8px); }
    100% { opacity: 1; transform: translateY(0); }
  }
  @keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0; }
  }
  .text   { font-family: "Courier New", Courier, monospace; font-size: 13.5px; fill: #c9d1d9; opacity: 0; animation: fadeSlide 0.45s forwards; }
  .title  { fill: #58a6ff; font-weight: bold; font-size: 15px; }
  .key    { fill: #7ee787; font-weight: bold; }
  .sep    { fill: #484f58; }
  .at     { fill: #f78166; font-weight: bold; }
  .cursor { fill: #58a6ff; animation: blink 1s step-end infinite; }
</style>

<!-- Terminal background -->
<rect width="100%" height="100%" rx="8" ry="8" fill="#0d1117" />
<!-- Top bar -->
<rect width="100%" height="28" rx="8" ry="8" fill="#161b22" />
<rect width="100%" y="20" height="8" fill="#161b22" />
<!-- Traffic lights -->
<circle cx="16" cy="14" r="5" fill="#ff5f56"/>
<circle cx="32" cy="14" r="5" fill="#ffbd2e"/>
<circle cx="48" cy="14" r="5" fill="#27c93f"/>
<!-- Title bar text -->
<text x="260" y="19" font-family="Courier New, monospace" font-size="11" fill="#8b949e" text-anchor="middle">neofetch — bash</text>

<!-- Prompt line -->
<text x="16" y="58" class="text title" style="animation-delay:0.05s">
  <tspan class="at">OxHazem</tspan><tspan fill="#8b949e">@</tspan><tspan class="key">github</tspan><tspan fill="#c9d1d9"> ~ $ neofetch</tspan>
</text>

<!-- Separator -->
<text x="16" y="78" class="text sep" style="animation-delay:0.2s">────────────────────────────────────</text>

<!-- Row: Name -->
<text x="16"  y="104" class="text key" style="animation-delay:0.35s">Name       </text>
<text x="130" y="104" class="text"     style="animation-delay:0.35s">Omar Hazem</text>

<!-- Row: Role -->
<text x="16"  y="126" class="text key" style="animation-delay:0.5s">Role       </text>
<text x="130" y="126" class="text"     style="animation-delay:0.5s">Data Scientist &amp; Software Developer</text>

<!-- Row: Education -->
<text x="16"  y="148" class="text key" style="animation-delay:0.65s">Education  </text>
<text x="130" y="148" class="text"     style="animation-delay:0.65s">CS &amp; DS @ Zewail City</text>

<!-- Row: Stack -->
<text x="16"  y="170" class="text key" style="animation-delay:0.8s">Stack      </text>
<text x="130" y="170" class="text"     style="animation-delay:0.8s">Python · C++ · Java · SQL</text>

<!-- Row: Focus -->
<text x="16"  y="192" class="text key" style="animation-delay:0.95s">Focus      </text>
<text x="130" y="192" class="text"     style="animation-delay:0.95s">Machine Learning &amp; Computer Vision</text>

<!-- Row: Learning -->
<text x="16"  y="214" class="text key" style="animation-delay:1.1s">Learning   </text>
<text x="130" y="214" class="text"     style="animation-delay:1.1s">C# · Systems Design</text>

<!-- Row: LinkedIn -->
<text x="16"  y="236" class="text key" style="animation-delay:1.25s">LinkedIn   </text>
<text x="130" y="236" class="text"     style="animation-delay:1.25s; fill:#58a6ff;">linkedin.com/in/omar-hazem-ahmed-229a...</text>

<!-- Row: Location -->
<text x="16"  y="258" class="text key" style="animation-delay:1.4s">Location   </text>
<text x="130" y="258" class="text"     style="animation-delay:1.4s">Egypt</text>

<!-- Separator -->
<text x="16" y="278" class="text sep" style="animation-delay:1.5s">────────────────────────────────────</text>

<!-- Color palette dots -->
<circle cx="130" cy="304" r="8" fill="#ff5f56" opacity="0" style="animation: fadeSlide 0.3s 1.6s forwards;"/>
<circle cx="150" cy="304" r="8" fill="#ffbd2e" opacity="0" style="animation: fadeSlide 0.3s 1.65s forwards;"/>
<circle cx="170" cy="304" r="8" fill="#27c93f" opacity="0" style="animation: fadeSlide 0.3s 1.7s forwards;"/>
<circle cx="190" cy="304" r="8" fill="#58a6ff" opacity="0" style="animation: fadeSlide 0.3s 1.75s forwards;"/>
<circle cx="210" cy="304" r="8" fill="#7ee787" opacity="0" style="animation: fadeSlide 0.3s 1.8s forwards;"/>
<circle cx="230" cy="304" r="8" fill="#f78166" opacity="0" style="animation: fadeSlide 0.3s 1.85s forwards;"/>
<circle cx="250" cy="304" r="8" fill="#c9d1d9" opacity="0" style="animation: fadeSlide 0.3s 1.9s forwards;"/>

<!-- Blinking cursor -->
<text x="16" y="340" class="text" style="animation-delay:2.0s">
  <tspan class="at">OxHazem</tspan><tspan fill="#8b949e">@</tspan><tspan class="key">github</tspan><tspan fill="#c9d1d9"> ~ $ </tspan><tspan class="cursor">▋</tspan>
</text>
</svg>'''

with open('info-card.svg', 'w') as f:
    f.write(svg)
print("Success! Created info-card.svg")