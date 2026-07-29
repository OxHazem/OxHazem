"""
Generates profile-ascii.svg — a terminal-style animated SVG card
showing the OxHazem name in block letters + key info lines.

Run from the repo root: python scripts/make_ascii_svg.py
"""

LINKEDIN = "linkedin.com/in/omar-hazem-ahmed-229a912wwwaa"
EMAIL    = "omarhazemhassan@gmail.com"

svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 300">
<style>
  @keyframes fadeIn {
    0%   { opacity: 0; }
    100% { opacity: 1; }
  }
  @keyframes scanline {
    0%   { transform: translateY(-100%); }
    100% { transform: translateY(400%); }
  }
  .bg   { fill: #0d1117; }
  .bar  { fill: #161b22; }
  .line { font-family: "Courier New", Courier, monospace; font-size: 5.5px; fill: #7ee787; opacity: 0; animation: fadeIn 0.05s forwards; white-space: pre; }
  .scan { fill: rgba(126,231,135,0.04); animation: scanline 3s linear infinite; }
</style>

<rect class="bg" width="420" height="300" rx="8" ry="8"/>
<rect class="bar" width="420" height="26" rx="8" ry="8"/>
<rect class="bar" width="420" y="18" height="8"/>
<circle cx="16" cy="13" r="4.5" fill="#ff5f56"/>
<circle cx="30" cy="13" r="4.5" fill="#ffbd2e"/>
<circle cx="44" cy="13" r="4.5" fill="#27c93f"/>
<text x="210" y="18" font-family="Courier New, monospace" font-size="10" fill="#484f58" text-anchor="middle">profile-ascii.svg</text>

<rect class="scan" x="0" y="0" width="420" height="30"/>

<text x="8" y="40">
<tspan x="8" dy="0"   class="line" style="animation-delay:0.00s">  &#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2557; &#x2588;&#x2588;&#x2557;  &#x2588;&#x2588;&#x2557;&#x2588;&#x2588;&#x2557;  &#x2588;&#x2588;&#x2557; &#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2557; &#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2557;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2557;&#x2588;&#x2588;&#x2588;&#x2557;   &#x2588;&#x2588;&#x2588;&#x2557;  </tspan>
<tspan x="8" dy="6.2" class="line" style="animation-delay:0.04s"> &#x2588;&#x2588;&#x2554;&#x2550;&#x2550;&#x2550;&#x2588;&#x2588;&#x2557;&#x255a;&#x2588;&#x2588;&#x2557;&#x2588;&#x2588;&#x2554;&#x255d;&#x2588;&#x2588;&#x2551;  &#x2588;&#x2588;&#x2551;&#x2588;&#x2588;&#x2554;&#x2550;&#x2550;&#x2588;&#x2588;&#x2557;&#x255a;&#x2550;&#x2550;&#x2588;&#x2588;&#x2554;&#x255d;&#x2588;&#x2588;&#x2554;&#x2550;&#x2550;&#x2550;&#x2550;&#x255d;&#x2588;&#x2588;&#x2588;&#x2588;&#x2557; &#x2588;&#x2588;&#x2588;&#x2588;&#x2551;  </tspan>
<tspan x="8" dy="6.2" class="line" style="animation-delay:0.08s"> &#x2588;&#x2588;&#x2551;   &#x2588;&#x2588;&#x2551; &#x255a;&#x2588;&#x2588;&#x2588;&#x2554;&#x255d; &#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2551;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2551;  &#x2588;&#x2588;&#x2588;&#x2554;&#x255d; &#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2557;  &#x2588;&#x2588;&#x2554;&#x2588;&#x2588;&#x2588;&#x2588;&#x2554;&#x2588;&#x2588;&#x2551;  </tspan>
<tspan x="8" dy="6.2" class="line" style="animation-delay:0.12s"> &#x2588;&#x2588;&#x2551;   &#x2588;&#x2588;&#x2551; &#x2588;&#x2588;&#x2554;&#x2588;&#x2588;&#x2557; &#x2588;&#x2588;&#x2554;&#x2550;&#x2550;&#x2588;&#x2588;&#x2551;&#x2588;&#x2588;&#x2554;&#x2550;&#x2550;&#x2588;&#x2588;&#x2551; &#x2588;&#x2588;&#x2588;&#x2554;&#x255d;  &#x2588;&#x2588;&#x2554;&#x2550;&#x2550;&#x255d;  &#x2588;&#x2588;&#x2551;&#x255a;&#x2588;&#x2588;&#x2554;&#x255d;&#x2588;&#x2588;&#x2551;  </tspan>
<tspan x="8" dy="6.2" class="line" style="animation-delay:0.16s"> &#x255a;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2554;&#x255d;&#x2588;&#x2588;&#x2554;&#x255d; &#x2588;&#x2588;&#x2557;&#x2588;&#x2588;&#x2551;  &#x2588;&#x2588;&#x2551;&#x2588;&#x2588;&#x2551;  &#x2588;&#x2588;&#x2551;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2557;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2557;&#x2588;&#x2588;&#x2551; &#x255a;&#x2550;&#x255d; &#x2588;&#x2588;&#x2551;  </tspan>
<tspan x="8" dy="6.2" class="line" style="animation-delay:0.20s">  &#x255a;&#x2550;&#x2550;&#x2550;&#x2550;&#x2550;&#x255d; &#x255a;&#x2550;&#x255d;  &#x255a;&#x2550;&#x255d;&#x255a;&#x2550;&#x255d;  &#x255a;&#x2550;&#x255d;&#x255a;&#x2550;&#x255d;  &#x255a;&#x2550;&#x255d;&#x255a;&#x2550;&#x2550;&#x2550;&#x2550;&#x2550;&#x2550;&#x255d;&#x255a;&#x2550;&#x2550;&#x2550;&#x2550;&#x2550;&#x2550;&#x255d;&#x255a;&#x2550;&#x255d;     &#x255a;&#x2550;&#x255d;  </tspan>
<tspan x="8" dy="8"   class="line" style="animation-delay:0.24s">&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;</tspan>
<tspan x="8" dy="8"   class="line" style="animation-delay:0.28s; fill:#58a6ff;">             Data Scientist &amp; Software Developer              </tspan>
<tspan x="8" dy="8"   class="line" style="animation-delay:0.32s; fill:#c9d1d9;">               CS &amp; DS @ Zewail City  |  Egypt                </tspan>
<tspan x="8" dy="8"   class="line" style="animation-delay:0.36s;">&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;</tspan>
<tspan x="8" dy="10"  class="line" style="animation-delay:0.40s; fill:#f78166;">  Focus:   </tspan><tspan class="line" style="animation-delay:0.42s; fill:#c9d1d9;">Machine Learning  Computer Vision  NLP      </tspan>
<tspan x="8" dy="8"   class="line" style="animation-delay:0.44s; fill:#f78166;">  Stack:   </tspan><tspan class="line" style="animation-delay:0.46s; fill:#c9d1d9;">Python  C++  Java  SQL  PyTorch  OpenCV      </tspan>
<tspan x="8" dy="8"   class="line" style="animation-delay:0.48s; fill:#f78166;">  Now:     </tspan><tspan class="line" style="animation-delay:0.50s; fill:#c9d1d9;">C#  Systems Design                           </tspan>
<tspan x="8" dy="8"   class="line" style="animation-delay:0.52s; fill:#f78166;">  Email:   </tspan><tspan class="line" style="animation-delay:0.54s; fill:#58a6ff;">''' + EMAIL + '''                    </tspan>
<tspan x="8" dy="8"   class="line" style="animation-delay:0.56s;">&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;</tspan>
<tspan x="8" dy="10"  class="line" style="animation-delay:0.60s; fill:#7ee787;">  Open to internships and research collaborations              </tspan>
</text>

<text x="8" y="258" font-family="Courier New, monospace" font-size="5.5px" fill="#7ee787">
  <tspan opacity="0" style="animation: fadeIn 0.1s 0.7s forwards;">$ </tspan>
  <tspan fill="#58a6ff">
    <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" begin="0.8s"/>&#x258b;
  </tspan>
</text>
</svg>'''

with open('profile-ascii.svg', 'w') as f:
    f.write(svg)
print("Success! Created profile-ascii.svg")