import re

with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

# Remove the entire block
dead_block_regex = r'<!-- Image Lightbox Modal for Customer Reference Photos -->\s*<div id="image-lightbox-modal".*?</div>\s*</div>\s*</div>'

html = re.sub(dead_block_regex, '', html, flags=re.DOTALL)

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(html)
    
print("Removed dead modal.")
