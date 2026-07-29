svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 600">
<style>
  @keyframes fadeSlide {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
  }
  .text { font-family: monospace; font-size: 14px; fill: #c9d1d9; opacity: 0; animation: fadeSlide 0.5s forwards; }
  .title { fill: #58a6ff; font-weight: bold; font-size: 16px;}
  .key { fill: #7ee787; font-weight: bold;}
</style>
<rect width="100%" height="100%" fill="#0d1117" />

<text x="20" y="40" class="text title" style="animation-delay: 0.1s;">OxHazem@github ~ $ neofetch</text>
<text x="20" y="70" class="text" style="animation-delay: 0.3s;">-------------------------------</text>

<text x="20" y="110" class="text key" style="animation-delay: 0.5s;">Role:</text>
<text x="120" y="110" class="text" style="animation-delay: 0.5s;">Data Scientist &amp; Software Developer</text>

<text x="20" y="140" class="text key" style="animation-delay: 0.7s;">Education:</text>
<text x="120" y="140" class="text" style="animation-delay: 0.7s;">CS &amp; DS Student @ Zewail City</text>

<text x="20" y="170" class="text key" style="animation-delay: 0.9s;">Stack:</text>
<text x="120" y="170" class="text" style="animation-delay: 0.9s;">Python, C++, Java, SQL, Ubuntu</text>

<text x="20" y="200" class="text key" style="animation-delay: 1.1s;">Focus:</text>
<text x="120" y="200" class="text" style="animation-delay: 1.1s;">Machine Learning &amp; Computer Vision</text>

<text x="20" y="230" class="text key" style="animation-delay: 1.3s;">Learning:</text>
<text x="120" y="230" class="text" style="animation-delay: 1.3s;">C#</text>
</svg>'''

with open('info-card.svg', 'w') as f:
    f.write(svg)
print("Success! Created info-card.svg")