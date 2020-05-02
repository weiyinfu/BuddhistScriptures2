import re

s="经/第1000-02部～佛说"
a=re.findall("\d+",s)
print(a)