import streamlit as st, sqlite3, hashlib, json, shutil, glob, base64, io, secrets, string
from urllib.parse import quote
from datetime import date, datetime, timedelta
from PIL import Image
import os
from contextlib import closing

# Logo Jahitin ID (tertanam di file ini supaya aplikasi tetap satu file; dipakai di favicon, login, sidebar, dan nota)
LOGO_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAQDAwMDAgQDAwMEBAQFBgoGBgUFBgwICQcKDgwPDg4MDQ0PERYTDxAVEQ0NExoTFRcYGRkZDxIbHRsYHRYYGRj/2wBDAQQEBAYFBgsGBgsYEA0QGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBj/wAARCAFoAWgDASIAAhEBAxEB/8QAHQABAAIDAQEBAQAAAAAAAAAAAAEGBQcIBAMCCf/EAF4QAAEDAwIEAgUHBwUIDwYHAAEAAgMEBREGQQcSITFRYQgTInGBFDJCUpGhwRUWI2JysbMzQ4KS0RckoqOy0uHiCRglJzc4RFNUVmNzdZTwKDQ1RXTCNkZVZISk8f/EABkBAQADAQEAAAAAAAAAAAAAAAABAwQCBf/EADsRAAIBAgMECAQFBAAHAAAAAAABAgMRBCExEkFRcRMiMmGBkaHRFDOxwQUjUuHwFUJy8TRigpKissL/2gAMAwEAAhEDEQA/AO51IUYU7qktuTjqoQHr1RCAibIhIRN0QWCbIEQAonxRARupC+FVWUlBSvqq2oip4GD2pJXBrR8SqTV8Q5bhVmg0ZZqi7T9jUOaWws89vvIWetiqVHKbze7VvwLadGdTsrIvZIawuc4ADuT0wqxdeIWlrU8wm4fLKgdPU0g9Yc+Ge33rEN0Rf7+71+sdQzOiPUUFEeVg8ie33H3q0WjS2n7E0C12uCF4/nSOaQ/0j1VHSYmt2IqC4vN+S+7LNijDtPafdp5/sVn86dc3zpp7Soo4T2qbg7HTxwcfip/M7WN266g1pJHGe8FAzlHuz0H3K+/SySm6fAbWdacpeNl5Kw+J2flxS9X6lLpuFmlIzz1cVXXP3dUTnB+DcLNUukNLUWDS6ft7CNzCHH7TlZpNlbTwWHp9mC8iuWIqy1kz5R09PCAIYIox4MYG/uX1wmyLSkloVakBN+6ndFJB+HxRyNxJGx48HNBWOqtNaerTmrsdvmJ3dA3P2hZTZN1xKnGeUlc6jJx0ZUKzhlpGqBMdDLRuP0qaZzcfA5Cx40HqK0gnTetKyJo6iCrHOz3f+gr/ALoFkl+HYdu6jZ8Vl9LF8cVVWTd135/UoJvPEeyj/dWwU13hb3moXYdjxwP7F7rZxJ01XS+oq5ZrZU5wY6xvKAf2u324VvXgudktF5h9XdLdT1Q8ZGe0Pc7uPtXPw+Ip50ql+6WfqrP6k9LSn24W5e2h7Y5YpoWywyskjd2exwcD8Qv2qBNw9rrRM6q0ZqCpt7883yWd3PE7y/8A9BX5Zr272CoZSa2sU1O09BX0jeaN3mR2+w/BPjnTyxMNnv1j57vFIn4bbzoy2u7R+XsbB37p8V47ddLddqIVdtrIqmE/SjdnHkR3B8ivWt8ZKSvF3RlaadmSibIpAQIiEBERCQm6KN0BKIiAHsibIgCZ6oiAJsm6nrhARsoz1U7JhCRuijdAUIJTZB4rF3zUVr09bjV3OoEYPSONvV8h8Gjf9y5nONOLlN2SJjFydorMyTnNawucQAOpJOAAqXdtfskrjaNI0TrzcScczB+hj8yd/uHmsayj1RxBcJ7k+WyWAnLKVn8rUDxd5eZ6eAPdXm02a2WShFHbKSOnjHfl+c8+Lj3JWDpK2K+V1YcXq+S3c35GrZp0e31pcNy5v2KjSaCrLxUtuOubk6vmBy2jhcWxR+XT8Me8q7UlHSUFG2loaaKngb2jiaGgfYvv4oD0WmhhadHOKzerebfiU1K06naeXDcD2RNlK0FI3UKd1CEhNkTbCAn4KE2UoERuiIgCJjoiAIiboQNlGylEA6L8SwxTwuhniZLE8Ycx45gR5gr6KD5I1cnkUa48PG01cbpo6vfZq7uY2uJif5Ebe7qPJfO368rLXcG2fXNuNvqD0ZWxjMMvn07e8dPcr5uvLcLbQXWhdR3KkiqYHd2SDPxHgfMLz5YJ03t4Z7L4f2vw3c0aliNpbNZXXHf5+56IpYp4GTQyMkjeOZr2EEOHiCO6/S11UWPUmhpnV2lpH3Kz55prZMeZ7BuWHf3jr4gq2ad1Ra9S0PrqGQtmaP0tNJ0kjPmNx5hWUcWpS6KqtmfDjye/6nFShsrbg7x/mpmk+CbputhQE2RNuyAJuiboQEREA2RNkQkhT1ToiC5HVSMoVCAlE2Q+SAFQh2VL1Vq6oguLdM6YYKq9zeySOraYeJ2zv16DufBU168KEduf7vuRZTpSqPZievVGs4LFIy20EBuF5mIbFRx9S0nsX47e7ufLuvDYdE1EtyGotYz/AJQujiHMgccxU/gAOxI+wefdZLSujqXTzH1tQ/5bd5xmesf1OT3Dc9h95+5WbZZaeHnWkquI8I7lz4v0W4ulVjTWxR8Xx9kCm6JuvQMoUqB3U9PFAR1UpsiEBFCHvlAOq8V0u9qsdsfcL1dKO20bOjqisnbDGP6TiBnyVe4l6+tfDLhjc9Y3Vjp2UjQ2ClYcOqZnHEcYPme52AJ2Wo9H8ErjxLjg4gekFNPdrnWNE9JptsjoqS2xO6tY5jSCXYIy3Ix9IuOcdJb2VTm77MVdm0qDjLwnulw+Q0HEfTM9RnlDBXsbk+RdgH7VdmPbI1r2ODmOAc1zTkEbEHcea1xcuAPBi6Wc2yfhvYo4COUPpYTBI3zD2kOB+K1lZGXz0ceMlh0TJdqy7cNdTzGmtz65/PLaarIwzm+qSW9OgIOcAtOVk9DnbnDt6dx0t1QAp2JB7ouS8nrhRumyIAc9k3TdOiAdU2TdEA6pum6ISgmET4oQR1wqdqTRRqaz8u6an/Jl6j9oPZ0ZN5OGxPjvurlsm6pr4eFeOzNft3osp1ZU3eJUNLa1F0qzZb5B+T71EeV0LxytlPi3z8vsyrfuq5qrSNDqaja4n5NcIRmnq2dHMOwOO7c/ZssVpfVdbHc/zW1Yz5PdY/Zimd82pGxz4nx396yU686E1RxDunpLj3Pg/qXzpxqxc6Xivbu+hedlHXCBF6JkCY6om6EhETohARNkQDdERCRumyKEBOyKFV9aar/N+2x0tvj+UXerPq6WADmOT05iPAbeJ+KqrVo0YOpN5I7pwlUkox1PHrHVlXTVsemNNRmovdT7OW9RTNP0j5469ew6nZZPSWk6TTVvJz8ouEwzU1burnnuQCfo5+3uV8NFaUOn7c+ruL/lF5rD6yqqHHmIJ68gPgN/E/BWkLLh6MqkviK2u5fpXvxfgXVaiiuip6b3x/YbYREW8zIJundCgHimyZUICdlK/OeinPTKBhRkBfCtraO3W+evuFTFS0lPG6WaeZ4YyNgGS5xPYALnyXiZxU40XWstnBOji09pinkMEusbrGeaYjv8nYQf3F3iWdlKjcqnUUOZYuN+mb5qviHwvt4tss2l6S9OuV5qHlrIYmxtb6sSFxAwcuwOvcraMmrNLMefW6osbHZyQ64Qjr/WWk4PRM0rdwyr4k621frO4E8z5KquMMWd+Vo5iB/SWaZ6J/AdkPq/zMlcPF1wnJ/yl07WsVRVS7klr3m5KeppqyljqqOpiqIJBzMmheHsePEOHQj3LRHpXTRu0BpC1QN57pXapo2UTW/P5hnmI/rN+0Lc2ndP2TRmjKDTtkhFHabZB6qBkkhcIoxk+052wySSVojTj5uO3pPt13E1x0LokvpbRMegrq5w9qZmdm9HA7BsfiVEVvOqzvFQ3s33LqXTcdTKyTUdna9ry1zXV0QIIPUEc3Qr8DU+mcZ/OSze/wCXw/5y0pcfRC4Y1RmlobhqGiqJSXuldUMqAXE5JIezr1PiufOKfo/6m4XQOur3U93sDnhguFPFymEk4AmZ15M9gQS0npkHoq22jfClTm7KWfI7u/OfTP8A1ks3/n4f85Pzn0yP/wAyWb/z8P8AnL+YAgj5f5Nn9UIYIyf5OP8Aqhc7Zf8AB95/T/8AOfTP/WSzf+eh/wA5Pzm0zn/8R2bH/wBdF/nL+YHqI89I2f1Qv0yl9ZI2KKnEkjyGtYxmS4noAAB1J8E2x8F3n9Pfzm01/wBY7N/56L/OT86NMBvXUtmH/wDPh/zlyhoL0RbndrdBc9dXP8iMkaHi20kLZKkA7SOPssPkA4jfC2hB6JXCKOMNnhvlSfF9cG/c1gXV2Z5Qpp22vQ3dSVlHX0wqKCsp6qEktEsErZGkjuMtJGV9z3Vb0PofT/DzSMemtNRVEVvZNJO1s8xldzPOXe0R2VkXRS7XyCIgQgIo7qUBGOqwOq9K0WqLT6mb9DVxe1T1LfnRO/s8Qs+irq0oVYOE1dM6hOUJKUXmUnSWqas3J+k9TtMN4pxiOR3apbsQdzjr5jzyrrsqzrLSw1DbmT0bhBdaX26WoB5Tnvyk+BO+xUaM1Q++2+SiuTPUXijPq6mEjBdg45wP3+B94WPD1JUZ/D1Xf9L4rg+9eqNNWKqR6Wmua4d/ItCbqD5KV6BlCIiAbIoPZEBKFE65QIIUKjOBnOPehBjr7eqTT9hnula79HGPZYD1kcezR5lVPRFkrLhcZNcaiZzV9X1pYnDpTx7EDbI7eXmV5Gf74uvHOdl2nbO/DR9Gpl/s/D3rZGABgdB4Lzaa+Lq9K+xHTvfHw0XmbJ/kQ2F2nr3Lh7jdTlN0XpGQIijZBcbKd0TdCAo2UpshKGygpspQHP3H2au1zxJ0XwHt9VLS019c653meE4cKSEk8vxLHn3hq3nabTbbFYqSzWeiioqCjiENPTRDDY2DsB+J7k5JWlL478mf7IfpapqmtEV00tPSUz3f84xzyWjzwPvW+CupaIopK8pSetzVer9U6y/OW7DTJEdBYI2SVQIaRKSMnOepAGwx0BK2LR3ekqdLwX2WaKnpJKZtU+WV4ayNhbzEucegA8SqC+6UtsrNaQS0lRUPuV0+QN9THzCMupnuDnn6LAGnr4kDdUuq4Tao4qU+n6XUurJ6DhzT2ymeLHbj6uavnGS/1z9mD2cdz3wB3WDCuTqNyet/R2NmIaULQWat6q+Zi9Uap1F6RmqJeH/Daee36DpZeS/aoLC0VYH8xT5+cD4b9zhvzugNM6asuj9KUOmtPUTKO20UXq4Ym9fMucfpOJyST3JK+1lsdo03YKWx2G3U9vt1KzkhpqdvKxg/EnuSepPdZDdbm9yMtOnZ7UtSF5bnbaG82artN0p2VFFVxOgnheMh7HDBH/rfC9fXKYUFp/MbVmn6jSuurxpypcTJb6ySm5j9JrXey74twfisQVtP0k6ZtJ6TOoeRuBMymnwPF0DM/eFqsdlS0ezTd4psnC3t6Kuj6bUPFyov9dGJYbDTieJjhkfKJCWxk/sgPcPMBaK+iuvfQ6o42aE1RXhmJJbjFCXfqthzj7XlTFZleJlam2jpIdk+iidcK08kFETdAE2T4ogGyJ1wiAbohQd0BBVE1tZay31set9PMxcKMZqYQOlRFvkbkDv5eYV86qNuuCPNUYmgq8Nh+D4Pcy2lVdOW0v8AZj7HeaS/WOnulEf0co6sJ6xuHdp8wsjutbsDuH3EP1eS3T94floJ9mml/s6/YfJbI3VeErupFxn245P35PU6r01Bpx7LzX87hnqmyDui1lIREQMJuiIAqVxBvdRT0NNpu0uJud1d6lob3ZGejj5Z7e7KuNRUQ0tLLU1EgZDEwve89g0DJK1/oWmm1Fqe467r2ECUmnoWO+gwdCR8MD3lywY2cpbOHg85ei3v7LmacPFK9WWkfV7i4afsdLp3T1PaqQezGMvfvI8/Ocff+7Cyhwm2EytsIRhFQirJGeUnJ7T1CIi6OQmyJsgCjCKUJCIiAhTsnvRAab9IbRd7vWkLVrjR3N+dOj6v8q0TWDLp4hgyxY3yGh2N8Ebq78OOINi4ncO6HVthlHqp28s9OXZfSzAe3E/zB7HcEHdWzsRg9fFc+6y4d6w4W65reKPBSjjq6asJlv8ApHqI6wDJdLAB2f3OB1BJLcglq6WasUSThLbWj19zYVC9rbhxIxkFkhccdO9OVYNDMczhnYGP7ihjz9mVToLs2S38QLkynfCaq2wVoik+cz1lJzcrvMZwfcrxpJpboCyB3f5BDn+oF5+GXXtz/wDZm+r2b8voZrbum6bp0ytxnCFE2QHBvpPgD0lbsR3NJSH/ABQWoBstu+k+c+ktdgP+iUn8ILUeeg9yplqevS7EeQ6Y812Z6IDccH72c97y7+DGuM8gDsuzvRBx/cbvB6//ABl/8GNTHUrxfyzoJMJsmytPLBRM5UoD8opRCRsiDsiBhRupRCAmybJsgMRqWxQai01U2ubAc8c0Un1JB80/b38iVheHl+qLjZJbPdMtudrd8nma49XNHRrvux8PNXAjp0Wu9YNfpTXNv1pSMIpp3fJrg1o6EbOPwH2tC87FroJrFLRZS5cfB+lzXh/zYui+a5/ubFCL8xvZJE2SNwexwDmuHYgjoV+l6JkCJsiAISieeQEJKHxJr6iogt+kLcf78u0oY/H0YgepPvP3Aq5W2gp7XaKa3UjQ2GnjEbfPG/x7/FUfSYOpOI941ZIOampj8joifDsSPh/lLYQ7Lz8H+bOeJe/Jcl7vM1YjqKNFbs3zfsNlCnPRR1XoGUlE3RCAo2UpshIRNkQEbqR2TCbIAoKlChBG6JunYoDSmsr3S2jVfEGkq5y19wt1OynbjPM7lAP3En4Ly3XjXdeGGo4bdrvQ1xh0U6lpRbtUW5hnjbmFnM2dgPQh3MOmDjHQ91geMseOKdcXHDX00J/wMfguh6Snhm07T0k8McsL6Zkb4pGhzHt5AMEHoR5Fedg5fnVE93u2aMVF9HBxdn+yPHprVmmdZWNt30rfKG70Tv56kkD+Q+Dh3afJwBWZBWk9SejZpeS+O1Nw2u9w4e6i6uFTZnkU0h8JIMgY8mkDyKwp4l8ceFJ9XxX0MzV1hi6HU2lxmRjfrSwYHx6M95Xp7N9DD0rj2147jobKKk6D4u8O+JdMJNHaoo66fHt0Lz6qpj8QYnYd08RkeauudlzaxapKSumcG+k+3/2lbrk/8jpP4S1COw9y2/6UOB6Sd0J/6HSfwlqHuB4YVUtT2aPYjyDicYIXZvogn/eavH/jL/4Ma4xOfguzvRB6cGbwcf8Azl/8GNI6lWK+WdB7Jso2Uq08wbhM9eybogBKIoQknZPcmyd0II3UpuiAbJsgTZAFjb7aYb5p2rtU/Rs8ZaD9V3cH4HCyR9ygrmcFOLjLRnUZOLTRS+G12lqdOTWStJFdaZDTSNd3LcnlP3EfAK67LXd0H5scaKC6sHJQ3lhp6g9gJOgBPx5T9q2IOmyxYCb2HRlrB28Nz8jRioraVSOks/f1GeiJsi3mUKt67vBsmhK6pY/lmlb8nhO/M/p09wyfgrHste63H5b4hab0sOsIk+WVA8h2z8Gu+1Y8fUcKL2dXkubyNGFgpVFtaLN+BZdGWf8AIeiKCgLcS+rEsvm93U/vA+Cz2yA9eyLRSpqlBQjolYqnNzk5PeERFYcDdERAE2RQgJTdE3QkDumECIAiKEBKJv3UIQc7caYCeJ5Lu0lJD+IXQ0DeSkiYOzWNH2ALQnGmMnijbmgfylLCP8a4Lf2MZHh0Xn4RWrVeZqrP8uBOFAyHZBIUqN16Bmsav11wA4b66ndcJbS6x3vPMy8WQilqGu+seUcrz7xnzVIEfpFcHKc+qMXFvTEPXlcTDdYGfeZMD9v4LohflTtPQpdGN7xyZwJxKrmcZOJlZq3SLXmodTQwz6eqx6m40z4mcrh6o/yo6Z/RknxaFqyQGKZ0TwWPYeVzHDBaR3BGx8lvX0ldQUf+2DuFlvenqS5UEVNSyRzwYpa6nc6MEuiqGjOc9eWQPb5BUl9JFerU+tq5qnW9vgj5n1cLGwahtjBvKzJbVxt+tl4x9KNcOKk8jfTxFShFdLG8eK+6Nf56ZBXZ/og5/uMXf/xl/wDBjXI1w09JDaxfbPWQ3iwvcGNuVMCBG49o54z7UL/J3Q/Rc5dceiD/AMC93wc/7tSfwYlyk1KzL684zpbUXdHQeyKB2U7Kw84hSiIAgREA2RCEQDdQpRCUEPZEQMJhEQgqXEi1G56AqpIsiooyKqJw7gt7/dn7FmdN3Rt60nQXQODjNCC/9sdHfeCsjJHHNE+GUBzHtLHA7gjBVE4ZPkoYbzpmYnnt1Y7kB+o4n8Rn4rz5/lYuL3TVvFZr0uao9eg1+l38H/EX7ZEx0RegZSPxVA0xm8cXdR3tx5o6QCjhP3H/ACT9qvNZUNpLdUVbzhsMTpCfcCfwVN4U07m6HfcJf5WuqpJnHx64/Arz8T18RSp8Ly8lZerNVHq0py5Lz/0XgKdkUL0DKNlKjZSgG6IiAbpsiIB0TdCiE2CJuiEEKdk2RAMKFO6IDR/F+Ln4qaeHQ+siib/j/wDSt4OGHuHmVp3itDz8VNIdM87mN/x7f7VuN2Oc+9Y8OvzanNF9XsQIREwthSFBCnplChBwX6T5x6S12x3+SUn8ILUcFVV0VZDWUVRLT1ULg+KaF5Y+Nw7Frh1B9y256UAz6St1z2+R0nf/ALoLUJHQe5VPU9il8uPIuVu1D+Vroa+puFNpvUbmmM3iOEGiuLT3iuFOAWkO3la3ze0/OHS3o16n0zaWXTh9WW92m9TVFWbiLXJKJKepa6No56OTJ54yGcwblxAPQuA6cbublmD9q6R4Q8LqDiv6NdTC+vnoNQWW8yOsV3Y8h9C8RxvDAR1ERcSS0diS4de/cJ3dpHn4rDdEnUpZcVufszsDZNlqTgnxRuer4LporXFMKDXenH+oudOQB8pZnDahgHQg9M46ZII6OC22u2rGWE1NXRKY6pumVB0EREAz0RNkQkIm6IAOybImyEBERCSN1Quln4+/Viu9H9r2j/V+9X5UDiMPkN30zqBoANLXCJ5/Vdg/gVg/EerTVX9LT9bP0Zpwuc3Dimi/7IhxnA7It5lK5r2qNJw3u8ucF0Hqwf2iG/ivvoykFFoCz02MEUrHH3u9o/vWC4sSubw9NOD1qKqOP95/BXOjh+T2+npwMCOJjPsaB+CwR62Mk+EV6tv7Gp5YdLi36JH3UbIgW8zWCJsm6AboiboAmyIgCboU3QXCImThAEUKUICJvhN0BqviZDz8UtCuH0qrlPwljK2oepWuOIUXrOJfD94//UXt/wAg/gtjDss9FWqT5r6Fs31Y/wA3koiLQVDKbIiA4L9KAgektdcf9DpP4QWovojPgtu+lB/xl7sf/wBpSfwgtQ/RHuVUtT2KPYjyJOcdSMLs/wBEHA4KXbA/+dSfwYlxhg9858l2h6If/Ardf/GpP4MSR1KsV8sj0hKWXh9qfTPH2xQFtVaKuO33tkYx8qoZTy+14luS0H9Zv1Qt+09RBV0cNXSyiWnmjbLFIOz2OALT8QQqTxotsN39HbWtDOwPa60TyAO+sxvO0/a0L4cC7nUXf0bNE19WSZnWqKNxO/Jlg+5oV7zR40erUa45mwd1KJ1yuS4BERANkTZChI3TdRupQBNkRAETqnXPVAFS+KVL8p4bVUjR7UEscw8sOx+KueTlYXWFOKnQN4hIzmle77Bn8FlxsNvD1I9z+hdh5bNWL70e+1VPyywUNX/ztPG/7WhFiNCVHyrhzaJCSS2D1ZP7JI/BFZh57dKM+KX0OKsdmbjwZguKbuaksFJnpNcm5+GB+K2C757h5rXfEwc140mzxuI/exbDPzz71mw+eJrP/H6F1X5NPx+o3REW8zEKSnTCISN0TdEICIiAbJunRN0A3UKVGEA6YRNlPuQDfomETIQFF1xF6ziBoE47XWT+Fn8FeR80FVTVUQfrPRbsfNucp/8A67/7FaxjAVVNdaXP7I7k8o/zeSiborStDdERAcE+lBn/AGzF2/8ApKT+EFqPYLbvpQf8Za7dP+SUn8ILUeOg9yplqexR7EeQ6YyO67P9EP8A4Frt4flqT+DEuMD2xhdneiLIyPgdd5pXsjjbeJXOc8gBoEMeSSewHipjqVYr5ZbfSO1NFpn0btR/pMVd0iFpo2DvJLMeXA9zec/BW/h1px+keEmmtMytxLb7dDBKP+05QX/4RctLW6qPpEekFS3mnj9bw40TUl9NM4exdLgMYcPFrcA/sgfXXSByepOSeuVe8lY8Wn15ua00QQ90Khcl43TClEA2RNkQEbqURAE2RNkJCIh7oCN15bpGJrFXRHqH08jcf0CvWvlUgGimB3jcPuK5mrxaJWTRUOFkhk4Y0efoyyt/wv8ASi+XCj/g5YM9BVSgfciy/h3/AAtPkvoXYr50+bPJxMPLeNJu8Lj+LFsQ/PK17xUaW0+n6vHSG4tJPh2P4LYR+eVxh8sTWX+P0Oqvyafj9Qmybp1W8zDHRE2RAERPegHTCjZSoQMnKZ69lCndAiM9eylR1UoCMrw3m9WnT1iqb1fLhT2+30zeeapqHcrWD+09gB1J6Be7BJwBknoAuFfSN4oz674hS6etlW/837LM6GONh9mpqG9HzHxwctb4AE7qG7FtKl0krGwNael5K2vko+H+n4HwMOBcLvzfpPNsLSMD9o58gqRSeldxZir/AF1SdPVUOcmB1vLB7uZr8rSHLhQe3RV7TPQWHppWsdt8LvSK0rxEvNJZdTWuCx34S5oi9/rIJpCCMRvPVjyCRyu75wCey3t2C/lcMiRrw5wc0gtc04LSOxB8V/RXgxqyr1rwPsN+uMnra50TqepkPd8kTiwuPmcAnzJXcXcx4iioZrQvqJui6MwUKSvz8EIOC/Sg/wCMvds/9EpP4QWpObDM42W5/SOs92vnpS3ahsluqK2obRUjnMhbzco9SMucezW+biB5qjWSwWr8pGi5ZNXXiNvNJabJMBS04Hd1VW/Ma0b8mR+uFXsuTyPS+Ip0acXN7vEwFrstzvMc01LHFDRU2DVXCqk9VTUrfGSQ9B5NGXHYFbw4Z6S1VxM0C7QGkrhcrPw5fVOqLxqOSH1Mt4eQ0OhpmHqIsMAwc+Lz9Ba4vt6tLBFT3aS3ahmo+tHZbc0x2O3O8cDBqn+LicHd7x0XW/ozVVzuPAWK63eplqKiruNS8OfgBrGlrGtY0ABjByYDWgAbBdxtF5amLEOrXjeS2Y8N758DZWmNM2PR2kqHTWm6COhtlFH6uGBm3i5x7ucT1Lj1JKzGyDomykqSSVkQpRN0JCJuiEDZE2TZAETdEJCbImUAREQBfKpPLRTnwjcfuK+q8V3l9Rp+vm+pTSO+xhXM3aLZMVdpFT4TgjhywneqlI+5F9+GEfquGdESPnySP6/tY/BFl/DlbC0+S+hbivnT5s8/FqIu4fCoHeCqjf8AvH4hXOjmFTb6eoHaSJrx8QCsDr6k+W8N7vEBkth9aPe0h34FevSFUKzQdoqQQeakY0nzA5T+5cQ6uMkuMU/Jtfc7lnh49zfqkZr4psiBbzNYJhEQgKFOE3QkjqnVSiEEeCndEQBEwoQlFZ4iXyXTXCTU1/gdyzUVtnmiPg/kIaf6xC/mk0uOPWOJf9Jx3O5X9FOOFJLW+jjrSCHPP+S5HjH6pDj9zSv52nGPa+1VzPQwaybDjvnHvWUj0zqWe2m4Q6cu76MDmNQ2jkMePHm5cYW//RW4XWjULq7X2oKOKtgoqj5Jb6eZgdGZQA58rmno7l5mgA9MknYLr4FzRytJAxjAOBhFG6Jq4rYlZI/lxaLVcr9dae12Wjmrq+odyQ08DeZzz7vDxJ6Ddf0U4UaMl0Bwgs2l6mRklXBG6SqdGctM0ji94B3AJxnyWdtml9N2a61t0tNht1DW1zuepqaanax8x/WIH3LLLpRsZq9fpFZLIlOqx17vln03Yp71f7pS22304zLVVUgYxvlk9z4AdTstFy8ctccTrjNZ+Aej5KijY8xS6tvkZho4z4xsPzj78n9VdpNmKdWMcnqb0vd+sum7PJdtQ3aitdDGMuqayZsTPgT3PkMlaVrPSNqtWVk1o4G6GuWtKxruR1znY6mt8J8S44JHvLV9bF6NlvuF5Go+MWqrlxCvRPMIqx7oqGDyZCD1H2D9Vbst9uoLTbIrZaqGmoaOIcsdNSxNijYPJrQAFOS7zi1SfcvU4T4n3e/RarrbXxdvlRer6BFJU2GxkUNtjJYHMbLK0c82GkdAOnbnWuLjqG5V9ALZE2nt1oa7mZa7dH6imB8XNHWR36zy4+as3G2ubdvSH1fWscHMFxdC0g56RtbH/wDaVRc9MKqU2z2MNhadNKSWfHefhzgwcx+K/olwMtUlm9HbSVJKzkkfQCpe07GVzpP3OC/n5Z7LU6j1LbLBRtJnuFXFSMA8XuDc/AEn4L+n9HSQUFvp6CmAbBTRNhjA2a1oaPuCiBzjZZJH22TZQpCsMARN0QAIiITcbIiIQETdEJCImyEA9k3REA6rB6yqBS8PrxMTjFK9v9b2fxWbVL4q1Bh4a1MLT7VTLHCB4+1k/wCSsuOnsYepLuf0LsPHaqxXejJ6Hg+T8ObRHjvTh/8AWJP4osraqb5HYKGk7epp44/saAitoQ2KUY8EjipLam5cWfWupm1lsqaNw6TRPi/rNI/FU7hRVOl0GaGX+UoqmSBw8OuR+8q853WvtIgWjirqaxH2Y6hwrYQd89Tj4P8AuWTEdTEUqnG8fNXX0L6XWpTjyf2+5sDIUqFIXoGYZ6IiZ8kA3ROilAQo2UqPBCCURRlAE2UogPFd7bT3rT9fZ6rHqa2nkppM/Ve0tJ+9fzCvNsq7Hf6+w3FhZV0E76SYEY9pji0n44z8V/UkgYXJPpV8LJILn/dPstMXQT8kN2Yxv8m8ANZMfJww1x8Q3xXMlvNeEqKMnF7zYvonVFLJ6PDKWBwMlNdKpswHfmcWvGf6JC3kFxX6KnEGHTWvarR10nZHQ35zTTvecBlU0ENGf12+z7w1dp58vgpi7oqxEXGowVRuKPFHT/C3STbndA+ruFS71NutUB/TVsvYNaOpDQSMux0yB1JAVsvF3t9g07XXy6ziChoYH1NRKfosaCT8enTzwtE8GdNVnErWs/pAa7pC6pqHOh0zb5erLfStJAlaD9I9cO8eZ24x2ktWZKk3dRjqxpzg/qvifeoNcekBVGdgPrLdoyncWUlC09vXAH2n47jOfrH6I37S0lLQUMNFQ00NLSwNDIoIGBjI2jsGtHQD3L7YU91DdzqFNQ01IC8l2udNZbFXXmseGU9DTyVUjjs1jS4/uXrJ6rQXpUa+jsPC/wDMyinAuV+9iUA9Y6Vpy8nw5iA0eXMoZdCLlJRRxfV1811uVTdJ3Ey1cz6h5Pfme4uP3lfjOG5KRxhsXT7ll9LaYves9WUem7DSmorat3K0fRYPpPedmtHUlUJ3PY0Rur0UNCOvnEWo1vVwk0VkaY6cuHR9U9pAx+wwk+9zV2gAq1oLRlr4f6At+lrUOaKlZmWYjDp5XdXyHzJ+wYGysuequSsjya1TpJXCJkeCZUlQRM9Uz1QBEHmEygGyJsiAHuijITPVASiJsgCIhQAqg8RB8vvWmbCMO+U1vrHj9VuB+JV96Kg9Lv6QAxl0Voo+p2D3D/X+5YPxHrU1S/U0vW79EasJ1ZufBNl/ONgibIt5mIOd1QNXYsvE7TuovmwzONFO4efQZ+DvuWwFVeIlpdduH9ayJpM9MBVREDrlnU4+GVi/EKblQbjqs1zWZfhZKNRKWjyfiWrHcJssNpW7i+aOt9zDgXyRASY2eOjvvH3rMrVTqKpBTjo8ymcXCTi9UMoo6qV2chFHXKdc7oBlNlI7Kq1PEPS9LxVo+Hstxj/LVVTPqGRBwIaWkYid9V7m8zgD3DT5ZEpN6Fq6qFOEQgKFKBCRsvNcLfRXS1VFtuNNHU0lTG6GaGQZbIxwwQR4L09UQhHD3Gn0e7toOqm1HpKOpr9N83rCIsunt3XPtY6lg2eO2/idn8FPSUtd4oKTS/EG4MpLq0Nip7tMcQ1mwEjuzJPM9HeR79IuAIwRkEYwtJ8Q/Rl0LrOSa4WTm0xdpMudLRxh1PKT9eHoBnxaR8Vza2hpVWM1s1PM+HpQ1c9bw50/oOhqXRT6tvlPbjyHq+EEOfjxGeRbpt1uo7PZ6W026FsNHRwspoI29msY0NaPsAXJf9zr0hOG1Tb2W+ntus7TbphUUdPI1lYIHt6h0UcuJYnf92Vn4vSp1XZZvk+tOEFypHNOHyQGWAf1ZWY/wlO2tClYV7TlFp3On8lN1zU/0zNHAFsejr4ZcdGvqIGjPvz+Cqt99LDXF8a6k0Zo6K384IE5a+unHmGhoaD7wU2kWLD1HuOkOIXEjTPDbTEl2v8AVt9cWn5NQRuHr6p+zWN8PFx6D7l/PzWGr7xr7W9fqm9vHyiqf0ib8yGMdGxs/VaPt6ndXBnC3jXxJv0l8rNO3usqqkj1lddz8nbj3yYw0eDRgeC2zoz0QB66Or19qLmYMF1ttBIDvJ0zh2/Zb8Vy7s00+jo5t5nO+j9E6n15qNlk0xbZKycnMjvmxQN+tI/s1vv6nYFd08IuD9l4VaedHE9tde6to+W3EtwXY6iOMfRjB27k9TsBcNN6V07o+yNtOmbRTWyjB5jHA355+s5x6ud5kkrMdVKjYz1sQ6mS0GOqlEXRnCbImyAIiboAoU9UQEbInXCkNc75rSfcMoCN1O6jrlOqAfBTsoHZTsMIAnVE67oD8SSMhifNI4NjY0ucTsAMlUThoySubetTzt9u41juQn6jTn8cfBZHiRdXWzQNSyJxE9Y4UsYHc83fHwB+1ZjTdrFl0lQWzGHQwgP/AGj1d95K8+f5uLjHdBX8XkvS5qXUoN/qdvBfvYymyKdkXoXMwUOaHNLXAOaRgg7hSncoDXuh3OsGsrzoyXIiY81dGTuw9wPgR9hWwh2VC4hU9Raq6160oW5fb5hHUgfTiccdftI/pK70tTBV0UVXTyCSGZgkY4bgjIXn4L8pyw7/ALdP8Xp5Zo1YjrqNZb9ea/lz69Mpsibr0DKeOiu1quNXV01uudHVzUcnqamKCZsjoH/VeActPkV9qyso7db5664VUNLSwMMks87wxkbR3LnHoAqG3hjHY+LdZxD0bVxUVbcYXRXO2VAcKWtcSCJMtBdG8OGSQCDk9Bkqnau4O8ReKF5Z+f2vbfb7DFJzR2awwSOb03c6THM/9ZwONgFB2oxb1yKxrbj/AKj1rqE6F4G2+qq6qbLH3dkeHlvYuiDukbB/zr8eQHdWDhv6M9lsTmag13Wz3vUbpBUc0NTIyOmkzzczXgh8kgPXnJx4DdbW0VoLS3D6wfknS9sZSxuwZp3HnmqHD6Ujz1cfLsNgFZFFuJ1KrZbMMkSTk5KKE6Z7ropClAiAbImyYQDooTHVEBWtRU/rdW6UeT0jrpT/AIlx/BWUlzo+RxLm/Vd1H2LGXOnMt5ssgGRFUyOJ8P0Lx+KyarhG0pPj7I7k7pHjdaLS6T1jrVQF/fmNNGT9uF6Yoo4BiCNkQ/7Nob+5fTdN1YcXI6k5Jz5lSgTyQDuERN0ARMdUQBERAERTugITdF4rtUV9JZKqptdu/KNbHGTBSetbEJX/AEWl7ujRnudhndAYPVl/vtKW2TRtrguWoJ2c4NU8spaKMnAmqHDrjIPKxvtPIOMAErTuo+CnG+/udcarjYZK75zaWAT0lOw+DfVnDR/RWK0Vx01BobX9x0lxrs5ts9ZVOqjcmRY9UX9BzgZEkIADWvbnlAAOeuOmqaop6yjiq6SoiqKeZgkilieHskaezmuHQg+IXOTL3tUtDkm08VuL3BXWNPYeLEFbd7NKcCeZwmfybyU84/lMdyx3X9krrK3XCiu1opbpbaqOpoqqJs8E8Zy2RjhkOHwKxmrdJWPXGkqrTmoqRtRR1A6H6cL/AKMjD9F7e4PwPQlUngBQ3Sx8K6zS12lM0livVbbI5MdHRseCCPLLz02zhSsiJyjOO1azNpAKR2TZTspKSCoPZSV4L1daeyWCrutSf0dPGX4+sdh8TgLmclCLlLRHUU5NJFLuxOpuM9BZ2+3Q2dnymoGxk6ED/JH2rYfU9SqRw0tc8On6i/1/tVt2lNQ5x7hmTyj45J+IV32WPARbg60tZu/huXkX4ppSVNaRy9/UImyLaZh8E3RFJJ5q+ip7lbKi31bOeCeMxvHkR/6KpXDuuqKCav0VcnH5TbXkwk/TiJ7jy6g+5yvyoWvrfVW2totcWhmaq3kNqWD+dhPQ592SPcfJefjYum44mP8Abr3x3+Wpqw7U06Mt+nPd56F8yp6Lx2y40t3s9PcqJ/PBOwPadx5HzB6L2LfGSklJaGVpp2Y7Ifch6pupBHZO/QAkrC6rut7sulqm6WDTzr/VwDnNvZUCCSRu/IS0guH1d+uOuAfLHZrveqFrtT3J0UUrPbtlqkfBEMj5r5uksmPIsH6qC289lZqS309a+30bZ7pcGfOo6Bolez/vHZDIh+24fFaNreJXEW9emDbNCWOup7bb6UNbcqSENqmcob62Uvc5o9sNLWZbgAnHVbVqr1ScMtJVf5XjYy0UMEk9JVxxhjZC1pcIZQ0ACU4wH9pPJ3Q6f9FWx1d2rtU8VLy0vrbnUvpYpHbku9bO4eXMWN/olQ+BdBJRcmdLZ6/gnTwRN8BSUDZN1GT2UoBuiEoN0BBa0kEgZHbOybKcdE2QBETdAE7IiAhTumyIBlE3RANk2REAT4Ih6jGSPMbIDwm82sajbp/5dCbo6nNX8kDsyCEODecjYZcAM99s4K9uVyhxR0jqrgpxQp+MOkrjcLvQzy8lx/KEpmkaX9DHK/HWJ46Ndj2HAD6q6Q0VrKya90VR6msMxfTVAw6Nx9uCQfOjeNnNP29COhUJlk4WSktDya94d6X4kaaNo1JRc5Zk09ZFhs9K8/Sjd+9p6HcLm6kuXEr0X9SMtt2ik1DoWpmIiezIYM7xk59TLuYz7LtvEdebLyXO2W692eotN3oYK6hqWGOanqG8zJG+BH49xsjRMKmzk80Vyz8SdKaj0fDqDTlwiuYqHCKCiY4NnfOe0LmHq13jnoAC7OBlZrT9pNmsTKWWRstTJJJU1UrRgSTyvL5HDy5nEDyAVB4W8EdO8M9QXq80n99VdZO9lHJJ7TqSkzlsQcepcfpO3AA8c7SzlEcy2U7R0GUz0RNlJygtd62kfqbWFt0TSSH1IcKmvLfotHYH4ZPvIVyv15prBp+putV82Jvst+u49Gt+JVc4e2eoioKnUl0HNcrq/wBc4kdWx5y0eWe/uwvOxj6accKt+cuX7vLzNWHXRxdZ7slz/YuUMccMDIYWBkbGhjWjsABgBftQFOF6CyMgRNkUgKN1OEQDdfiWOOaF8MrGyRvaWua4dHA9CCv2mEauSa30/UP0PrqbSVZI78l1zvXW+Z/Zrj9DP3e8DxWyFgdWaag1Pp91G8iOpjPrKabeN/8AYex/0LHaH1NUXSmmst6b6m9UBMczH95GjoH/ANvwO687Dv4ap8PLsvs/ePhu7uRrq/nQ6VarX39y3p1TdN+q9ExkdVHVfrdQgOfPSw1bLQ8PLbom3uL66+1IdJEw+0YY3DDcfrSFg/olbd4eaUi0Rwwsml4wOeipWtncPpzO9qR3xeXfcq5rPg3YNU8TNPa8hDKa7WythmqQ4Ex1sTDkNcNntwC12+MHYjZPXuTlQlmWykthRQ65VN4qavodEcI71fa7DnfJ3U1PCTgzTSAsYwfEknHYNJVyXJnGO51/GL0hrdwu0+2eqtVme51b8lc3LnjBneC4huWN/RtyR7RI3RsUo7Us9DZXo31XEi6cMobxrK+ivtkwLLbHVQl1UWNPL6x0uerCQQA4E9M5wt1dcgeKxGn6uxvtUdssnLBHQRNg+QPYYpaVjRyta6N2HN6DvjB2JWmvSj1ybDoS3aUtM0ovl1qo54XU7i2WCOJ4Ie0t6hzn8rW4/WTRC3STy3m/Nx1Uqp8OrbrG16AoabXV+/K95MbXyyGFrDDkD9GXD+UI7FxAJOVaHyMiifLK8MYxpc5xPRoAySpK2rOx+8+aLyW+5W27UQrbVcKSupnDImpZmysPxaSF6tkIJTdRunxQEooPmpQDZMoo2QE7qeq+Us8EHIZ5oohI4MYZHhvO49mjPc+Q6r6b4KAbqNlStSzazt/ELT1bDd6Nmk5awUtdSxUuKhrntLYnOlcSDGZeVpDQ0jmb1Iyrrg9EJaJTdMIO6EHmuFuobvaam13Oliq6OqjdDPTyjLZGOGCCFyX/ALuei3xq/wCVV+g70/8AaPKPu9fED/Tb93XqrHEHR1BrvhxdNNV9PHMZ4XOpnPPKYp2gmN4d9Eh2OvgSN1DRbTns5PRmdt1wobvZ6a62uriq6GqjEsFREcskYRkEFela+4RcLoeF+im2x13q7lXTYfUvfK8QRuPUthiJwxud8czu58FsJEVysnkOuUTfZFJAUdcKeypmudRVdNFFpuxZkvVw9hgYesLD3cTscZx4dTsqcRXjQg5y/wB9xbSpupLZRibgXa/4hx2qJ3NYrQ/nqXg9Jpe3L+Hu5itkABoDWgAAYAGyw2l9O02mNOQ22Ah8nz55d5JD3Pu2Hks1jqqcHQlBOpU7cs39l4HeIqKTUYdlae/iOqbIg7LYZwiIosAiJupARMIgIVL1tpurlni1Vp4mO80Q5i1o/wDeGDYjcgfaOngrqoPkqcRQjXg4S/0+KLKVR05bSMLpbUtFqixsrqbDJm+zPAe8T/D3eBWa6Kgansdx09eTrHSsWXA5r6JvzZm7uAH3/aN1bbHfLfqG0MuFvkDmno+Mkc0bt2u/9dVRhsRLa6Ct216rivutxbWpRt0lPsv07iJb1BTahZaqyJ9P69oNNUPI9XO7dgOzh4HvssnsvNX0FHc6B9FXQtmhf3aehBHYg9wRsQsTQz3a03KO03Jk1fSSnlprixvM4fqTAdjjs/sd1c5ypytPNPR8O5/Z+ffWoqS6upYNlG6lOmVeVGveMXEGbh1wzrbrRW+tqbhLG6Gkkip3PhgkPQSSvHRgbnIz3IwqL6LehPyLw7m1zcgZbpqE+sZK/q5tMHHlyfF7svP9Fb6e1r2OY9rXMcOVzXDIcPAjceS89BQUNrt0VvtlHDSUkIIjggYGMYCScNaOgGSegUWzLFO0NlHiv9FZJba+53oinZQxOm+XseYpaVjQS5zZG4LQACcZwdwVzFwgt1fxl9Iq4cTb+6eqtFke1tF8pa3LnjPydhDQG5a39I7AHtEeKtnpS6zvlFo2HRVpslzZBdZWMqbo6Llp5GZHLAyQH5znY5s46DHXK2zwy0PS8POGNs0xDyunhZ62smaP5aof1kd7s+yPJoUassi9iF97Ldv5rFanvcGmtE3fUNSQI7fRy1Rz0yWsJA+JwPisrutIelTqQWXgQ+1seBNeauOlwD1MTP0sn+S0f0lLKqcdqSRUvRG0fTmxXnXtdTA1lRVGkpX9QGNa3mlcB2yXPDc+DcLpvZUrhBps6T4Haas0jOSoFG2oqBv62X9I7Pxdj4K7IlZE1ZbU2yi2i6cTbxqS8ObbNOW+yQV0tLQSVgqHVNUxjuX1ha0gNaSDg74yBjqapoDjNqPXmu9RaYo9KWlktkLw+odcJWMm5ZTEOUeqcRktJ67LczTyva52xBJ9y5c9Ez+/NZcQbueplliGf2ppn/2I2dRScZO2hvTSesrnftU33T160pU2GutDYHu56plRHUMl5+V8bmgZb7B7jy6EFW7pgr8+qiE7phGwSuaGF4A5i0EkAnwyT08yv1spKm7mjNM8XNcXj0nKrhfd7dYaCnoDO6aamZLI+obGwObyl7sN5g5pzg46ree3Vcv3w/kD/ZIbRU45WXSGFp8/WUz4v8pgXUA6gKEWVUlZrgag49cLLXrvSUN0ZJHb7tQzxEXFwc4MhLuR3OAfmt5g7I6jlJC1lZeLnE/gnfIdJ8X7RVXW055Ke5Md6yXlHTMcp6TNH1XYePHZdTVlJT19uqKGrbzQVEToZR4tcC0/cSq9R223au4eiyart1Nc2s5qKugqWB7XSxExl3kTgOBGD7QwUaJhUytJXRFBetNcTeH1TLpu809dSVcRiE0Rw6CTu3naerHNcGnBA7LMWG6OvOmqO5SMDJpox66MfQlB5ZG/B7XD4LmvVPAXW3Da/wAms+CN5rXtb7UlqLw6cN78oz7NQz9Vw5vDJV89H/ibU68g1Jb7xb47dd6KrbUzUrOZoHrW4kIa7qz9IxxLT2L1F88xKmtnai7o3RupwMqFO66KQmEQIBsoOMKdlX6+tudyuctlszJKVsRAqrlIzAjyM8kQPzn437BV1Kigr6vgdwg5MyEV2pptQPtNO180kTC+eRg9iE9OVjj9Y98bAdV789V5LZbaK0W5lDQw+ribknJy57j3c4nqXHclfG+Xug09ZpblcJOWNnRrB86R2zW+a5U3CDnVdvoiXFSlswR5dU6kpNM2N1bMPWTvyynpx3lf4e7xKw+idN1tM+bUuof0l5rvaId/MMP0R4Ht7hgeK8mmbLcNQ3saz1MzGetBROHswt2cQftHievgr/sslGMsTNV6itFdlf8A0+/hwRfUkqMeijq9X9vcbomEXomUBMdE3UoQRsiIhI2TdMKUIIREQDZQmylAQVr2+6duGl71Jq3SMZcw+1W21vzZG9y5o+/A7dxuFsLHVAs+Iw0a8bPJrR70y2lVdN9z1XExGntSW3U1qFbbpeowJYXfPid4Efj2Ky/YKjag0hX0d3Op9GPbS3EdZqTtHUjcY7ZPh2PkVk9LayotRNfRzRmiukPSajl6EEdy3PcfeFTRxMoyVHEZS3PdLl39xZUopx6SlmvVfziWc9l5rhcKC1W2a5XSsp6Kjgbzy1NRII442+LnHoF6FUdfWutrqaxXCltb7xDabrHcKm1s5eeqY2N7QWBxDXPjc9sjWkjJZ064W5GWTssjN2PUVh1NQvrdP3iiucDHcj30sofyOxnDh3acdcEBZPYqnXS72G0WCt4nPs1fDXNofk3qqiB9NU1P6TEULo3d3OkLWtJGRznHQlZGlvdRbYtOWbUr436hubC2SOhiPqxJHHzzO6n2YmnDeYnu5v1lJClxM3UU9PV0clLWU8VRBKOWSGZgex48CD0K+vYAAdNk2Pl38s+KFQdDuuUOO9b+fPpK6L0TJBV09qpqqKmlnqoHwxSySytMnI5wAcAxjWgjoSThdX7r8TQxVEfqqmKOaMEODJWh4BHUHB3UNXLKc9h3P30HRreVuzfAeCJ1PVDnCkrPLdJ/ktirqknHqqaWTP7LCfwXOXobU5/MvVVwI6zV9PHn9mIu/wDvW/dXW673jQ11tNjqqSlr6ymfTR1FW1zo4g9pa52G9SQCceeFQ+BfDHUHCrTl1sV4rrXXQVNU2qgnozIHA8gYWua9o+qCCDuVD1LYtKnJb8ja6fBQgUlRy96QzvyF6TnDbU4HKMwtc7x9XVDP+DKuo3Dlkc3wJC1Lxf4NVPFi8WWd+pmWeltbJOQR0hmme97mknmLgAByNwMd8raFvhq6e1U8FfW/LqmOMNlqfVCL1rgOruQEhufAFQtS2ck4xW9Ho3VDq9VU2mOM505LR19RHfqVlcx1FSvqPk87D6lxlDAeRr2iMhx6ZY7Kvm6nqMgHGe+N1JWnYjfHRYoabsbNXnVUdthjvDqc0slZGOV80RIPLJjo/BaCC7JGxWWUbZQi4TfsoL2CRkZe0PfnlaSAXY74G6o1Rry9SxXG6af0bLdrHbpJYpqsVzIZqkxOLZTTQlp9YGlrgOZzOYtIbsSsQ5Jalvu1zpbJYay8V/rRS0kLqiYxROkcGNGXENb1OACengV6IKiGqpYqqmlZNBMxskcsbuZr2uGQ4HcEEHKoctfcrXqOPWdgoblqTTOoKSKWeloQJZaeUMHqp4o3uGY5IyGvaD0c1rsdXLK8OrRcLHoCC33CkNCG1FRJS0DpBI6ipnyudDTucCQSxhA6EgfNBIGVNsjlSu7FqPZSeyjZYDU+rrbpmlb64morZekFHEcveds+A8/sVVWrClFzm7JF0ISm9mKuz2X2/W7TtqfX3KYMb1DIx86R31Wjf8FTrHY7jq+9M1VquIspG9aG3O+aBs5w8N+vU+5eiyaSuF6vDNT62IkqR1prf/NwN7jmHj5fblXzCwxpzxclOqrQWkePe/svM0SnGgtmDvLe/svcbKR2Qdk2XpGQlRuiboAibqUBGyJsiE3HZEKboQERNkA2RNkwgCJuiAKr6o0XRahLa2CZ9BdYsGKsh6HI7B2O48+4VoUbKqtRhWi4VFdHdOpKnLai8zX9t1pc9P1zbNr2AwPJxDco25jlHicfvHxAV9iliqIGTQSMlieOZr2HIcPEFfG4W6hutA+iuNLHUQP7skGfiPA+YVFk0zqfR0j6rR1W6voObnfa6k5IH6vj8MH3rFevhcnecP8AyXPj9TTanW06svR+xb9Q2Gj1Jp6az1sk8McjmSsmp3BskMkbxJHIwkEBzXtaRkEdOoIWHt2naqwV1w1ZeLncNU3htJ6iLlpooXNgaecwwxMw3me7BcScuIaOgAC/Vh19ZbzP8jqfWWy4A8rqWrHKebwBPf44KtXittGvCtHapu6MtWjKEuurM01w7h0vVcT65lqkbcamMy3dl7pXSwVWJZSH0VxYcczml/sBw+bGPZaWZdaaLUWsjxNu2n4aK13u10Dqd09Wx5op6Qz8zhFynmZMWRhriQWEh7ehKvhyR1657+axlksVHYn176aSeWS4V8lwqZZnBznSPwMdh7LWta1o2DQrrlKg1ZI8kmuNHRap/N2TU9rZdfWCH5I6cBwkPaMnsHn6hPN5LPLTX5Nv9FwaruFjtC3GtudRHPStuLWsNBO+V7nCukmLstcC4SOBb6wPbgZ6FZLX2pLtp3WelmU12k+QWWmN0v7nHAqKUvjpOaTwAL5Zuv8AzR8FNiFUsrs2mmyoelta3XVPE26UNPb2U+nKS2w1FNPK0ieqfLK9rZcH+Tjc2J5a0jmc0hxwCAs1rbV9BoXR0uo7nTzz00U8EL2QDL/0kjWcwG/KCXEeDSubHamrX3FjULBXPV9hteprDYJ6sy199ke2higbz87GxmR0rj9GPA+duSAM9cfW7aosdjvtns9zrfU1l4mdBRx8jnc7gB84gYaMlrQTgFzmjuQhO0jMIsNf9U2rTTqFlxbXSzV8r4qaCho5KqWVzWF7gGRgnAaCcqLPqqy36irai2zzOfQktq6WenfBUU7uXmDXxSAOaS3qMjBHYlLDaV7Ga2Tqq1pfWDtV01NXUel79RWyqpm1VPcK+OGOOVrgC3DWyOflwORlo88L9a91BW6V4cXbUVvp6aeehibNy1PN6sM52h7ncvXDWlzsDvypYjaVrlkQg4ycgHdUO16nuldofUlxtWoLTqi50dNJJSR2y3yQQCUROcyMFz3et5nAdQ7y3VT+UWui0/pjU2mNc3K86kuNXRs5JLo6cXQSPYKiN9LzFkYYwyO9lrfVer2wQZscuoX678RdJ2S4VtFV1tXNNQAOrhRUM9S2hbyh3NO6NhEY5SHdTnHXGFYn8tdbHGkrHRtnizFVU5aS0Ob7L2Egg9wRkEdu619qXReorpxEu0NnvtXZrHf7TyXCqpIIpXipizEzHP8AM54pMEtGT6rGW9Crtp+jrLdpWgt1wZQMnpoGwFtAHiANYOVvIH+0BygdCTjtk90yEXJtplIt7tTUvGuxW7V0tJVintVcbbdqdnq/lry+n5xJF2ilbG0k8pLXAktxgtHtOhb/AEkdxs9i1kLdp+4TTTOp/kAlqqT1zi6VlPMXhrWuc55HMxxYXHGemL2QMhSPndEuSoLeea3W+jtVnpLVQQiGjpIWU8EQOQxjGhrR8AAvQcNYS4gAdSSegVf1DrOyacBjqZjUVZ6NpKfDpCfP6vxVbZa9X65/S36R9js5OW0UJ/Syt/W/0/YsNXGxjLo6S2pcFu5vca6eHbW1N7Mf5ot567trmpr7k+w6Iphca/GJKo/yMHnnsff296yGmdE09nqjdrpUG5XmU80lVJ1DCfqA/v7+5Zy02a22O3NorZSsgiHU4+c8+Lj3JXv3UUsJKUlVxDvLcty5d/eyZ10o7FJWXq/5wB7ohRbjMERB2QBN0U9zhAFCIgJRRsiAZRE3QBERANk+CDsiEgoiIQFGylNkJIU7qFKCxhb9payajgLLnSNdKBhs8fsyN9zt/cchVUWjXWkDzWSt/L9uH/JKk4kYP1ev7j8FsRFjrYKnUl0i6suKyf7+JdDETgtl5rgym2ziPZKmf5Fd45rNWjo6KraQ3P7X9oCt0U0NRA2anmZLE7q18bg5p+IXkudltN5h9Vc7fT1TcdDI3Lh7ndwqjJw4lttQanSOoa20yHr6l7vWRnyP+nKr2sVR1Smu7J+Wj80d2oT0ey/Ne5e+mewXxko6OaWWSWkgkfLH6mRz42uL2ZJ5HEjq3qeh6dT4qkfljiTYhi6WCmvULf56idyvx5gf5q+1NxS0960Q3Wmr7XNu2phJA+I6/cpX4lQTtUbi/wDmVvXT1DwdR5xW0u7MtNJZ6ChvNyutPG4VVxdE6pe55PN6tnIwAbADYbkndeLUunhqJtoifUMjhobnDcJY3s5xO2MPxH5ZLmnPXt5r70OptPXLAobzRSk/REoafsOCsqPablvtDxHVbIVYzzg7maVNrKSsa5s/C6PT+qNP19HcJK6O3TTukmrnZmbD8nfDS08eBj1cTZHDvk5Ljkkrx6l4d6r1VddR3R+oqW1y1TI6S2wCkbUephgeJYX+sJBY9036RwAOMMHXlW0vJB3Vm0yro42sUfUdLqqrn0VqKn08yruFunkqLhb4qyKLkMtI+JwZI88rgJHD3hezTVovMmsrxq3UNHTW+W4U1NQxW+Cf5QY4YTI7mlkADXPcZXdG9GtAGSSVbECXOtjO5q/hloO+aMjt9PVaf05D6imNLUXKC41E9TM0dW8rHRhjQcMyObAwcLYN7tNLf9MXGxVxeKa4UstJKWY5g2RhaSM7jOQvfsmD3IPvUN7xGCirHypYTS2+npPXSTeoiZEJJD7TuVoGTjpk4ycLzU9lstHdZ7nR2e309dUfy1VDTRsll/aeBzO+JStvdntwzXXWjp8bSTNB+zOVW6vifpWCUw0c1TcZtmUkJdn4nCz1cXRpduaXiXww9SfZi2XJHFrWFziA0d3E4AVBOpNfXpvLYtKNt8Tu1TcHYIHjg4/cU/MG83otk1fquqqmb0lJ+jj+3/QqPjZT+RTcu95L1z8kW/DqPzJJer9DK3niBpy0v9RHUur6onDYKMc5J8Ce371heTiHq2UCQs03a3dwCfXvH7/3K32jTdjsUYZa7dDA4fzmOZ597j1WVx1yoeGq1vnzsuEcvN6v0CrU6fy458X7afUrmn9FWHTp9dS0xqKw9XVdSeeQny2b8FYlKjZbKVKFKOzTVkUTqSm9qTuydkRFYcDdB3U7qEATZEQBFOyjdAMoiDshI2REQXCboiBDdERCBsiIhI3TCIgCbIiAKN0RAgM5U9URAOuE6oiAjrlfKopaasjMdXTQ1DD05ZWB4+8IihpNWZCdtCt13DrR1fkvs0cDvrUznR/cDj7ljP7ltDTu5rVqC9UJ2DJuYD9yIscvw/DSd3TV+7L6GhYqtHJSZJ0frSmGKHiBVOGwqIy78SpFl4nRjDNX0EnnJT/6qIuP6dS/tcl/1S9zr4ue9J+C9gbZxT5cfnJacjf1P+qo/I/FF/R2q7awfqQf6qIp/p8P1y/7mR8VL9MfJH5Oj9c1Q/v7iBO1p7iniLf7FP8AcwiqHc111Te647gy8o/FET+m0H2k3zbf1Y+Lq7nbkkZCj4a6PpHBzrW6pcPpVMrn/d0CsdFbbdb2clBQU1MP+xiDPvARFopYajS+XBLkiqdapPtSbPV1REV5wEREIG6IiAdcJ1REA3TdEUAfFAiKQEREA6oiISwiIhB//9k="
LOGO_URI = "data:image/jpeg;base64," + LOGO_B64
st.set_page_config(page_title="Jahitin ID - Custom made for you", page_icon=Image.open(io.BytesIO(base64.b64decode(LOGO_B64))), layout="wide")
_cfg = ".streamlit/config.toml"   # tema bawaan Streamlit (input, dropdown, dll); berlaku setelah restart
if not os.path.exists(_cfg) or "624341" not in open(_cfg, encoding="utf-8").read():
    os.makedirs(".streamlit", exist_ok=True)
    open(_cfg, "w", encoding="utf-8").write('[theme]\nbase = "light"\nprimaryColor = "#624341"\nbackgroundColor = "#f7f4ef"\nsecondaryBackgroundColor = "#ffffff"\ntextColor = "#2d2a2a"\n\n[server]\nenableStaticServing = true\n')
DB = "siapjahit.db"
MARUN = "#064E3B"       # Emerald
DENIM = "#14532D"       # Deep Green
TOSCA = "#10B981"       # Emerald Accent
KUNING = "#D4AF65"      # Gold # palet logo Jahitin ID: marun, hijau tua, hijau sage, emas
STATUS = ["Diterima", "Dipotong", "Dijahit", "Finishing", "Siap diambil", "Diambil"]   # sesuai swimlane: Diterima > Dipotong > Dijahit > Finishing > Siap diambil
BATAL = ["Dibatalkan", "Dioper ke teman", "Ditolak (penuh)"]
UKURAN = ["Lingkar dada", "Lingkar pinggang", "Lingkar pinggul", "Lebar bahu", "Panjang lengan", "Panjang baju/celana"]
PAKAIAN = ["Permak potong celana", "Ganti resleting", "Permak lainnya", "Kemeja", "Baju koko", "Celana", "Gamis", "Kebaya", "Rok", "Seragam"]
WARNA_STATUS = [KUNING, DENIM, MARUN, TOSCA, "#2f7d4f"]   # warna kolom Papan Kerja
BACKUP_HARI, BACKUP_MAKS = 7, 10   # backup berkala otomatis tiap 7 hari, simpan 10 salinan terakhir
JENIS_LAPOR = ["Reset password pelanggan", "Nonaktifkan akun pelanggan", "Aktifkan kembali akun", "Kendala teknis", "Permintaan lain"]

JENIS_AKUN = JENIS_LAPOR[:3]

FASE = {
    "Ringkasan": "Pantau aktivitas dan pengingat pembayaran",
    "Papan Kerja": "Kelola proses pengerjaan pesanan",
    "Dashboard": "Pantau perkembangan usaha jahit",
    "Pelanggan & Ukuran": "Kelola data pelanggan dan ukuran badan",
    "Pesanan": "Catat dan kelola pesanan pelanggan",
    "Pembayaran & Nota": "Kelola pembayaran dan nota transaksi",
    "Belum Lunas": "Pantau tagihan yang belum diselesaikan",
    "Lapor ke Admin": "Sampaikan kendala dan permintaan bantuan",
    "Ukuran saya": "Kelola data ukuran tubuh",
    "Pesanan & Nota": "Lihat pesanan dan riwayat pembayaran",
    "Akun": "Kelola informasi akun",
    "Akun Saya": "Atur informasi dan keamanan akun",
    "Backup & Restore": "Kelola cadangan data aplikasi",
    "Laporan": "Pantau laporan dan aktivitas usaha",
    "Log": "Lihat riwayat aktivitas akun"
}
KAPASITAS = 12        # wawancara: kerja bersamaan 10-12 pesanan
LONJAKAN = 5          # cm; selisih ukuran baru vs lama yang perlu dikonfirmasi (kasus 76 ditulis 70)
WA_ADMIN = "https://wa.me/6281234567890"  # ganti nomor admin

# ---------- Gambar latar ----------
def _svg_latar():
    """Ilustrasi perlengkapan jahit (dipakai kalau tidak ada foto static/latar.jpg)."""
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice">',
         '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#eadfd8"/><stop offset="1" stop-color="#cbbab2"/></linearGradient></defs>',
         '<rect width="1600" height="900" fill="url(#g)"/>',
         '<path d="M0 560 C260 470 520 680 820 590 S1360 470 1600 580 V900 H0Z" fill="#624341" fill-opacity=".42"/>',
         '<path d="M0 690 C300 610 560 790 900 700 S1400 620 1600 720 V900 H0Z" fill="#1f4a42" fill-opacity=".36"/>',
         '<path d="M0 790 C320 740 620 860 980 800 S1440 750 1600 810 V900 H0Z" fill="#4a8a79" fill-opacity=".32"/>']
    t = '<g transform="rotate(-9 800 200)"><rect x="-150" y="150" width="1900" height="80" fill="#d9b565"/>'
    for i in range(0, 1900, 22):
        t += f'<line x1="{-150 + i}" y1="150" x2="{-150 + i}" y2="{150 + (30 if i % 110 == 0 else 16)}" stroke="#5a3b12" stroke-width="2.5"/>'
    s.append(t + '</g>')
    for x, y, c in [(110, 300, "#624341"), (1330, 120, "#1f4a42"), (700, 470, "#4a8a79"), (1440, 560, "#b8893a")]:   # gulungan benang
        s.append(f'<g transform="translate({x},{y}) rotate(-8)"><rect x="0" y="36" width="120" height="150" rx="10" fill="{c}"/>'
                 + "".join(f'<line x1="0" y1="{48 + k * 22}" x2="120" y2="{48 + k * 22}" stroke="#fff" stroke-opacity=".28" stroke-width="3"/>' for k in range(6))
                 + '<rect x="-16" y="14" width="152" height="26" rx="12" fill="#ead9bd"/><rect x="-16" y="182" width="152" height="26" rx="12" fill="#ead9bd"/></g>')
    for x, y in [(1150, 430), (1240, 500), (380, 560), (900, 330)]:   # kancing
        s.append(f'<g transform="translate({x},{y})"><circle r="44" fill="#f4eadb" stroke="#c4b095" stroke-width="5"/>'
                 + "".join(f'<circle cx="{dx}" cy="{dy}" r="6" fill="#8a7a66"/>' for dx, dy in [(-12, -12), (12, -12), (-12, 12), (12, 12)]) + '</g>')
    s.append('<g transform="translate(980,250) rotate(-22)"><path d="M0 0 L210 -70 L216 -58 L24 26Z" fill="#aab2ba"/><path d="M0 0 L210 70 L216 58 L24 -26Z" fill="#c4cbd2"/>'
             '<circle cx="-30" cy="-34" r="32" fill="none" stroke="#4a3f40" stroke-width="12"/><circle cx="-30" cy="34" r="32" fill="none" stroke="#4a3f40" stroke-width="12"/></g>')
    s.append('<path d="M240 420 C420 300 520 520 700 400 S1000 330 1180 470" fill="none" stroke="#624341" stroke-width="6" stroke-linecap="round"/>')
    s.append('</svg>')
    return "".join(s)

def latar():
    d = os.path.dirname(os.path.abspath(__file__))
    for f in ("latar.jpg", "latar.jpeg", "latar.png", "latar.webp"):
        if os.path.exists(os.path.join(d, "static", f)): return f"/app/static/{f}"
    return "data:image/svg+xml;base64," + base64.b64encode(_svg_latar().encode()).decode()

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&family=Cormorant+Garamond:wght@600;700&display=swap');
@property --n{syntax:'<integer>';initial-value:0;inherits:false}
@keyframes naik{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes hitung{from{--n:0}}
@keyframes isi{from{width:0}}
@keyframes denyut{0%{box-shadow:0 0 0 0 rgba(98,67,65,.5)}70%{box-shadow:0 0 0 9px rgba(98,67,65,0)}100%{box-shadow:0 0 0 0 rgba(98,67,65,0)}}

.stApp{isolation:isolate;font-family:'Lato',system-ui,sans-serif;color:#2d2a2a;background:#f4efe9;}
.stApp::before{content:"";position:fixed;inset:-20px;z-index:-1;pointer-events:none;background:url(__BG__) center/cover no-repeat;filter:blur(5px) saturate(.95);}
.stApp::after{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background:linear-gradient(rgba(248,243,240,.74),rgba(248,243,240,.86));}
[data-testid="stAppViewContainer"],[data-testid="stMain"],.main{background:transparent !important;}
h1,h2,h3,h4{color:#2e1f1e;font-weight:700;}
header[data-testid="stHeader"]{background:rgba(255,255,255,.9);backdrop-filter:blur(8px);height:52px;border-bottom:1px solid rgba(0,0,0,.08);}
[data-testid="stAppDeployButton"],#MainMenu{display:none;}
.block-container{max-width:1240px;padding-top:4.2rem;}
.element-container{animation:naik .35s ease both;}

/* bilah atas & judul halaman */
.usr{position:fixed;top:0;right:74px;height:52px;display:flex;align-items:center;gap:9px;z-index:1000000;font-size:13px;color:#2e1f1e;}
.usr .av{width:30px;height:30px;border-radius:50%;background:#624341;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;}
.pt{font-size:19px;font-weight:700;letter-spacing:.04em;color:#5b4a4f;margin:4px 0 16px;text-transform:uppercase;}
.pt small{display:block;font-size:12px;font-weight:400;letter-spacing:.02em;color:#8a7a7e;text-transform:none;margin-top:2px;}

/* kartu angka berwarna */
.mk-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:4px 0 18px;}
.sc{border-radius:4px;overflow:hidden;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.18);animation:naik .5s ease both;transition:transform .2s,box-shadow .2s;}
.sc:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(0,0,0,.2);}
.sc .top{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:16px 18px;background:var(--c);color:#fff;}
.sc .top svg{width:62px;height:62px;flex:none;opacity:.95;}
.sc .r{text-align:right;min-width:0;} .sc .n{font-size:24px;font-weight:900;line-height:1.1;font-variant-numeric:tabular-nums;} .sc .t{font-size:14px;font-weight:700;margin-top:3px;}
.sc .bt{display:flex;justify-content:space-between;align-items:center;padding:12px 18px;font-size:13px;color:#4a302e;}
.sc .bt svg{width:18px;height:18px;flex:none;}
.ang{--n:0;display:inline-block;animation:hitung 1s ease-out forwards;} .ang::after{counter-reset:n var(--n);content:counter(n);}

/* progress bar */
.bar{background:rgba(0,0,0,.09);border-radius:99px;height:9px;overflow:hidden;margin:4px 0 16px;}
.bar i{display:block;height:100%;border-radius:99px;background:var(--c);animation:isi 1.1s ease-out both;}

/* stepper status */
.stp{display:flex;gap:6px;margin:8px 0 14px;}
.stp .st{flex:1;text-align:center;position:relative;}
.stp .st span{position:relative;z-index:1;display:inline-flex;width:30px;height:30px;border-radius:50%;background:#fff;border:2px solid #d8cfcb;align-items:center;justify-content:center;font-weight:700;font-size:13px;color:#8a7a7e;}
.stp .st::before{content:"";position:absolute;top:14px;left:-50%;width:100%;height:3px;background:#d8cfcb;}
.stp .st:first-child::before{display:none;}
.stp .st.done span{background:#4a8a79;border-color:#4a8a79;color:#fff;} .stp .st.done::before{background:#4a8a79;}
.stp .st.now span{background:#624341;border-color:#624341;color:#fff;animation:denyut 1.8s infinite;}
.stp .st small{display:block;font-size:11px;margin-top:5px;color:#6b5a5f;}

/* komponen bawaan Streamlit */
div[data-testid="stMetric"]{background:#fff;border:1px solid #e6dcd8;border-radius:4px;padding:12px;}
div[data-testid="stExpander"]{border-radius:4px;border:1px solid #e3d8d3;background:rgba(255,255,255,.92);}
div[data-testid="stForm"]{border:1px solid #e3d8d3;border-radius:4px;background:rgba(255,255,255,.92);}
div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div[data-testid="stVerticalBlock"] .ctitle){background:#fff;border-radius:4px;box-shadow:0 1px 4px rgba(0,0,0,.15);}
.ctitle{font-size:14px;font-weight:700;color:#4a3a3a;}
div[data-testid="stDataFrame"]{border-radius:4px;overflow:hidden;}
button[data-baseweb="tab"]{font-weight:700;}

/* sidebar */
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#33201f,#4a302e);}
section[data-testid="stSidebar"] :is(h1,h2,h3,p,label,span,div,small){color:#f6efe6;}
.brand{display:flex;align-items:center;gap:11px;margin:4px 0 14px;}
.brand .lg{width:48px;height:48px;box-shadow:0 4px 12px rgba(0,0,0,.35);}
.brand b{display:block;font-size:16px;letter-spacing:.06em;text-transform:uppercase;color:#fff;}
.brand small{color:#eadfd2;font-size:11px;}
.nv{font-size:11px;letter-spacing:.12em;color:#d8c7b5;margin:10px 0 6px;}
section[data-testid="stSidebar"] div[role="radiogroup"] label{padding:9px 14px;border-radius:5px;margin-bottom:3px;transition:background .2s;}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{background:rgba(255,255,255,.1);}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){background:#d2a94f;box-shadow:0 3px 10px rgba(0,0,0,.25);}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) *{color:#2e1f1e !important;font-weight:700;}
section[data-testid="stSidebar"] div[role="radiogroup"] label>div:first-child,section[data-testid="stSidebar"] div[role="radiogroup"] label>span:first-child{display:none;}
section[data-testid="stSidebar"] .stButton>button{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.4);}
section[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,.14);border-color:#d2a94f;color:#d2a94f;}

/* tombol */
.stButton>button,.stDownloadButton>button,.stFormSubmitButton>button,.stLinkButton>a{border-radius:4px;transition:all .2s;}
.stButton>button:hover,.stDownloadButton>button:hover,.stFormSubmitButton>button:hover,.stLinkButton>a:hover{border-color:#624341;color:#624341;}
button[data-testid="stBaseButton-primary"],button[data-testid="stBaseButton-primaryFormSubmit"],button[kind="primary"],button[kind="primaryFormSubmit"]{background:#624341;border:0;color:#fff;font-weight:700;}
button[data-testid="stBaseButton-primary"] *,button[data-testid="stBaseButton-primaryFormSubmit"] *,button[kind="primary"] *,button[kind="primaryFormSubmit"] *{color:#fff;}
button[data-testid="stBaseButton-primary"]:hover,button[data-testid="stBaseButton-primaryFormSubmit"]:hover,button[kind="primary"]:hover,button[kind="primaryFormSubmit"]:hover{background:#4a302e;color:#fff;}

/* nota, info, daftar */
.nota{background:#fff;border:2px dashed #c8ad8a;border-radius:4px;padding:16px;animation:naik .4s both;font-variant-numeric:tabular-nums;}
.nota h4{margin-top:0;}
.sol{display:flex;gap:14px;align-items:center;padding:16px 18px;margin-bottom:8px;border-radius:4px;background:var(--c);color:#fff;box-shadow:0 1px 4px rgba(0,0,0,.18);animation:naik .5s both;}
.sol b.n{font-size:28px;font-weight:900;opacity:.9;} .sol small{color:#fff;opacity:.92;} .sol b{color:#fff;}
.kartu{background:#fff;border:1px solid #e6dcd8;border-left:4px solid #624341;border-radius:4px;padding:10px 14px;margin-bottom:6px;animation:naik .4s ease both;transition:all .2s;}
.kartu:hover{transform:translateX(3px);box-shadow:0 3px 10px rgba(0,0,0,.1);}

/* identitas Jahitin ID: logo, huruf serif seperti logo, kolom papan kerja, lonceng notifikasi */
.lgi{display:inline-block;flex:none;background:url(__LOGO__) center/cover no-repeat;border-radius:50%;}
h1,h2,h3,h4,.pt,.brand b,.hero h1,.nota .kop b{font-family:'Cormorant Garamond',Georgia,serif;}
.pt{font-size:26px;letter-spacing:.08em;}
.hero{text-align:center;margin:2px auto 20px;}
.hero .lgi{width:176px;height:176px;box-shadow:0 8px 28px rgba(51,32,31,.28);animation:naik .6s ease both;}
.hero h1{font-size:38px;letter-spacing:.16em;margin:12px 0 0;color:#624341;text-transform:uppercase;font-weight:700;}
.hero p{letter-spacing:.3em;font-size:12px;color:#1f4a42;text-transform:uppercase;margin:2px 0 4px;font-weight:700;}
.hero small{color:#8a7a7e;}
.kol{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;border-radius:4px;background:var(--c);color:#fff;font-weight:700;margin-bottom:8px;}
.nota .kop{display:flex;gap:10px;align-items:center;margin-bottom:6px;} .nota .kop .lgi{width:46px;height:46px;} .nota .kop b{font-size:20px;color:#624341;}
.usr .bel{background:#d2a94f;color:#33201f;border-radius:99px;padding:1px 9px;font-weight:700;font-size:12px;}
@media (prefers-reduced-motion:reduce){*{animation:none !important;transition:none !important;}}
</style>"""
st.markdown(CSS.replace("__BG__", latar()).replace("__LOGO__", LOGO_URI), unsafe_allow_html=True)

# ---------- Database ----------
def db():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c
def q(sql, a=()):
    with closing(db()) as c: return [dict(r) for r in c.execute(sql, a).fetchall()]   # koneksi ditutup (penting di Windows)
def run(sql, a=()):
    with closing(db()) as c, c: return c.execute(sql, a).lastrowid
def hp(pw): return hashlib.sha256(("siapjahit" + pw).encode()).hexdigest()
def catat(aksi, aktor=None):
    run("INSERT INTO log(waktu,aktor,aksi) VALUES(?,?,?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M"), aktor or st.session_state.get("user", {}).get("username", "-"), aksi))

# ---------- Notifikasi, pesan kilat, backup ----------
def notif(uid, pesan):
    """Notifikasi dalam aplikasi (lonceng) untuk satu pengguna."""
    run("INSERT INTO notif(user_id,pesan,tgl,dibaca) VALUES(?,?,?,0)", (uid, pesan, datetime.now().strftime("%Y-%m-%d %H:%M")))
def notif_role(role, pesan):
    for r in q("SELECT id FROM users WHERE role=? AND aktif=1", (role,)): notif(r["id"], pesan)
def flash(pesan, jenis="success"):
    """Pesan yang tetap tampil setelah st.rerun()."""
    st.session_state.setdefault("_flash", []).append((jenis, pesan))
def tampil_flash():
    for jenis, p in st.session_state.pop("_flash", []):
        {"success": st.success, "info": st.info, "warning": st.warning, "error": st.error}[jenis](p); st.toast(p)
    if st.session_state.pop("_balon", False): st.balloons()
def daftar_backup(): return sorted(glob.glob("backup_*.db"), key=os.path.getmtime, reverse=True)
def buat_backup(label="manual", aktor=None):
    f = f"backup_{datetime.now():%Y%m%d_%H%M%S}.db"
    s, d = sqlite3.connect(DB), sqlite3.connect(f)
    try: s.backup(d)
    finally: d.close(); s.close()
    catat(f"backup {label} {f}", aktor); return f
def backup_berkala():
    """Langkah 42: backup otomatis bila salinan terakhir sudah lebih dari BACKUP_HARI hari."""
    fs = daftar_backup()
    if not fs or (datetime.now() - datetime.fromtimestamp(os.path.getmtime(fs[0]))).days >= BACKUP_HARI:
        buat_backup("berkala", "sistem")
        for lama in daftar_backup()[BACKUP_MAKS:]: os.remove(lama)

def init():
    with closing(db()) as c, c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, nama TEXT, hp TEXT, pw TEXT, role TEXT, aktif INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS ukuran(id INTEGER PRIMARY KEY, pelanggan_id INT, jenis TEXT, data TEXT, diisi_oleh TEXT, diperiksa INT, tgl TEXT);
        CREATE TABLE IF NOT EXISTS pesanan(id INTEGER PRIMARY KEY, pelanggan_id INT, jenis TEXT, catatan TEXT, tgl_selesai TEXT, status TEXT, total INT);
        CREATE TABLE IF NOT EXISTS bayar(id INTEGER PRIMARY KEY, pesanan_id INT, jumlah INT, tipe TEXT, tgl TEXT);
        CREATE TABLE IF NOT EXISTS log(id INTEGER PRIMARY KEY, waktu TEXT, aktor TEXT, aksi TEXT);
        CREATE TABLE IF NOT EXISTS laporan(id INTEGER PRIMARY KEY, dari TEXT, pesan TEXT, tgl TEXT);
        CREATE TABLE IF NOT EXISTS notif(id INTEGER PRIMARY KEY, user_id INT, pesan TEXT, tgl TEXT, dibaca INT DEFAULT 0);
        """)
        for tbl, col in [("pesanan", "bahan_siap INT DEFAULT 1"), ("pesanan", "dibuat TEXT"), ("pesanan", "selesai_real TEXT"),
                         ("pesanan", "foto BLOB"), ("laporan", "jenis TEXT"), ("laporan", "target INT"),
                         ("laporan", "balasan TEXT"), ("laporan", "tgl_balas TEXT"), ("laporan", "status TEXT")]:
            try: c.execute(f"ALTER TABLE {tbl} ADD COLUMN {col}")
            except sqlite3.OperationalError: pass
        c.execute("UPDATE pesanan SET status='Siap diambil' WHERE status='Selesai'")   # data versi lama
        c.execute("UPDATE pesanan SET status='Diterima' WHERE status='Baru'")           # nama status mengikuti swimlane
        if not c.execute("SELECT 1 FROM users").fetchone():
            for u, n, r, p in [("admin", "Admin", "admin", "admin123"), ("penjahit", "Bu Aya", "penjahit", "jahit123")]:
                c.execute("INSERT INTO users(username,nama,hp,pw,role) VALUES(?,?,?,?,?)", (u, n, u, hp(p), r))
init()
try: backup_berkala()
except Exception as e: st.session_state["_err_backup"] = f"{type(e).__name__}: {e}"

rp = lambda x: "Rp " + f"{int(x):,}".replace(",", ".")
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
def tgl_id(d=None):
    d = d or date.today(); return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"

# ---------- Komponen tampilan ----------
ICO = {"keranjang": '<circle cx="9" cy="21" r="1.2"/><circle cx="20" cy="21" r="1.2"/><path d="M1 2h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/>',
       "jam": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
       "uang": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><path d="M6 10v.01M18 14v.01"/>',
       "orang": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
       "ukur": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
       "kotak": '<path d="M21 8l-9-5-9 5v8l9 5 9-5V8z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
       "file": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/>'}
def ikon(n): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICO.get(n, ICO["file"])}</svg>'
PANAH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 12h8M13 8l4 4-4 4"/></svg>'

def ang(n):
    n = int(n)
    return f'<style>@keyframes h{n}{{from{{--n:0}}to{{--n:{n}}}}}</style><span class="ang" style="--n:{n};animation-name:h{n}"></span>'

def M(label, v, w=MARUN, ik="file", sub=""):
    return dict(label=label, v=v, w=w, ik=ik, sub=sub)
def metrik(items):
    h = "".join(f'<div class="sc" style="--c:{i["w"]};animation-delay:{k * .08}s"><div class="top">{ikon(i["ik"])}<div class="r"><div class="n">{i["v"]}</div><div class="t">{i["label"]}</div></div></div>'
                f'<div class="bt"><span>{i["sub"] or "&nbsp;"}</span>{PANAH}</div></div>' for k, i in enumerate(items))
    st.markdown(f'<div class="mk-grid">{h}</div>', unsafe_allow_html=True)

def bar(label, persen, warna=MARUN):
    st.markdown(f'<small>{label} - <b>{int(persen)}%</b></small><div class="bar"><i style="--c:{warna};width:{min(max(persen, 0), 100)}%"></i></div>', unsafe_allow_html=True)
def stepper(status):
    i = STATUS.index(status)
    h = "".join(f'<div class="st {"done" if k < i else "now" if k == i else ""}"><span>{"✓" if k < i else k + 1}</span><small>{t}</small></div>' for k, t in enumerate(STATUS))
    st.markdown(f'<div class="stp">{h}</div>', unsafe_allow_html=True)
def wa(nomor, teks):
    n = nomor.strip().lstrip("0"); return f"https://wa.me/62{n}?text={quote(teks)}"
def judul(t, sub=""):
    sub = sub or FASE.get(t, "")
    st.markdown(f'<div class="pt">{t}' + (f'<small>{sub}</small>' if sub else "") + '</div>', unsafe_allow_html=True)
    if "user" in st.session_state: tampil_flash(); panel_notif()

def panel_notif():
    u = st.session_state.user
    rows = q("SELECT * FROM notif WHERE user_id=? ORDER BY id DESC LIMIT 8", (u["id"],))
    n = q("SELECT COUNT(*) n FROM notif WHERE user_id=? AND dibaca=0", (u["id"],))[0]["n"]
    with st.expander(f":material/notifications: Notifikasi" + (f" ({n} baru)" if n else ""), expanded=n > 0):
        if not rows: st.caption("Belum ada notifikasi.")
        for r in rows: st.markdown(f"{':red[●]' if not r['dibaca'] else ':gray[●]'} **{r['tgl']}** - {r['pesan']}")
        if n and st.button("Tandai semua dibaca", key="nt_baca"): run("UPDATE notif SET dibaca=1 WHERE user_id=?", (u["id"],)); st.rerun()

def ubah_status(o, s):
    """Langkah 26-31: ubah status, simpan, dan beri tahu pelanggan."""
    run("UPDATE pesanan SET status=?, selesai_real=? WHERE id=?", (s, (o["selesai_real"] or str(date.today())) if s in STATUS[4:] else None, o["id"]))
    catat(f"status pesanan {o['id']} -> {s}")
    if s == "Siap diambil":
        notif(o["pelanggan_id"], f"Pesanan {o['jenis']} Anda siap diambil." + (f" Sisa tagihan {rp(o['sisa'])}." if o["sisa"] > 0 else " Sudah lunas."))
    else: notif(o["pelanggan_id"], f"Status pesanan {o['jenis']} Anda sekarang: {s}.")
    flash(f"{o['pelanggan']} - {o['jenis']}: status sekarang {s}.")
    if s == "Diambil" and o["sisa"] > 0: flash(f"Masih ada sisa tagihan {rp(o['sisa'])} untuk pesanan ini.", "warning")

def teks_wa_siap(o):
    return f"Halo {o['pelanggan']}, pesanan {o['jenis']} Anda sudah siap diambil." + (f" Sisa pembayaran {rp(o['sisa'])}." if o["sisa"] > 0 else "") + " Terima kasih 🙏 - Jahitin ID"

def catat_bayar(p, j, t):
    """Langkah 21-25 & 34-36: catat pembayaran, hitung sisa; jika lunas dan Siap diambil maka otomatis Diambil."""
    run("INSERT INTO bayar(pesanan_id,jumlah,tipe,tgl) VALUES(?,?,?,?)", (p["id"], j, t, str(date.today())))
    sisa = p["sisa"] - j; catat(f"bayar {t} {rp(j)} pesanan {p['id']}"); st.session_state["_pilih_bayar"] = p["id"]   # tetap tampilkan nota pesanan ini
    if sisa <= 0:
        pesan = f"Pesanan {p['jenis']} {p['pelanggan']} LUNAS."
        if p["status"] == "Siap diambil":
            run("UPDATE pesanan SET status='Diambil', selesai_real=COALESCE(selesai_real,?) WHERE id=?", (str(date.today()), p["id"]))
            pesan += " Status otomatis menjadi Diambil, nota akhir siap."
        notif(p["pelanggan_id"], f"Pembayaran {rp(j)} tercatat. Pesanan {p['jenis']} Anda lunas, terima kasih! Nota akhir ada di menu Pesanan & Nota.")
        flash(pesan); st.session_state["_balon"] = True
    else:
        notif(p["pelanggan_id"], f"Pembayaran {t} {rp(j)} tercatat untuk {p['jenis']}. Sisa tagihan {rp(sisa)}.")
        flash(f"{t} {rp(j)} tercatat. Sisa tagihan {rp(sisa)}.")

def halaman_akun():
    u = st.session_state.user
    st.markdown(f"**{u['nama']}** · {u['role']} · username `{u['username']}`")
    with st.form("gp", clear_on_submit=True):
        lama = st.text_input("Password lama", type="password"); baru = st.text_input("Password baru (min. 6 karakter)", type="password"); ulang = st.text_input("Ulangi password baru", type="password")
        if st.form_submit_button("Ganti password", type="primary"):
            if not q("SELECT 1 FROM users WHERE id=? AND pw=?", (u["id"], hp(lama))): st.error("Password lama salah.")
            elif len(baru) < 6 or baru != ulang: st.error("Password baru minimal 6 karakter dan harus sama dengan pengulangannya.")
            else: run("UPDATE users SET pw=? WHERE id=?", (hp(baru), u["id"])); catat("ganti password"); flash("Password berhasil diganti."); st.rerun()

def balas_laporan(l, txt):
    """Langkah 39-44: Admin menjalankan aksi akun (jika ada), mencatat log, lalu membalas penjahit."""
    jn = l["jenis"] or "Umum"; hasil = txt.strip()
    if l["target"] and jn == "Reset password pelanggan":
        pw = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        run("UPDATE users SET pw=? WHERE id=?", (hp(pw), l["target"])); catat(f"reset password {l['t_hp']}")
        hasil = f"Password baru untuk {l['t_nama']}: {pw} (minta pelanggan menggantinya di menu Akun Saya). " + hasil
    elif l["target"] and jn in JENIS_AKUN[1:]:
        on = int(jn.startswith("Aktifkan")); run("UPDATE users SET aktif=? WHERE id=?", (on, l["target"])); catat(f"{'aktifkan' if on else 'nonaktifkan'} akun {l['t_hp']}")
        hasil = f"Akun {l['t_nama']} sudah {'diaktifkan kembali' if on else 'dinonaktifkan'}. " + hasil
    hasil = hasil.strip()
    if not hasil: return False
    run("UPDATE laporan SET balasan=?, tgl_balas=?, status='Selesai' WHERE id=?", (hasil, datetime.now().strftime("%Y-%m-%d %H:%M"), l["id"]))
    for x in q("SELECT id FROM users WHERE username=?", (l["dari"],)): notif(x["id"], f"Admin membalas laporan #{l['id']} ({jn}): {hasil}")
    return True
def menu(opsi, ik):
    st.sidebar.markdown('<div class="nv">NAVIGASI</div>', unsafe_allow_html=True)
    return st.sidebar.radio("Menu", opsi, format_func=lambda o: f":material/{ik[o]}: {o}", label_visibility="collapsed")
def grafik_pemasukan():
    d = {r["t"]: r["n"] for r in q("SELECT tgl t, SUM(jumlah) n FROM bayar GROUP BY tgl")}
    data = {str(date.today() - timedelta(days=29 - k)): d.get(str(date.today() - timedelta(days=29 - k)), 0) for k in range(30)}
    with st.container(border=True):
        st.markdown('<div class="ctitle">Pemasukan (pembayaran diterima) 30 hari terakhir</div>', unsafe_allow_html=True)
        st.bar_chart(data, color=MARUN, height=240)

def pesanan_lengkap(where="1=1", a=()):
    rows = q(f"""SELECT p.*, u.nama pelanggan, u.hp pelanggan_hp,
                 COALESCE((SELECT SUM(jumlah) FROM bayar WHERE pesanan_id=p.id),0) dibayar
                 FROM pesanan p JOIN users u ON u.id=p.pelanggan_id WHERE {where} ORDER BY tgl_selesai""", a)
    for r in rows:
        r["sisa"] = r["total"] - r["dibayar"]
        r["hari"] = (date.fromisoformat(r["tgl_selesai"]) - date.today()).days
        r["aktif"] = r["status"] in STATUS[:5]            # belum diambil & tidak batal
        r["proses"] = r["status"] in STATUS[:4]           # belum siap diambil
        r["mendesak"] = r["hari"] <= 3 and r["proses"]
        r["telat"] = (r["status"] in STATUS) and ((r["selesai_real"] or str(date.today())) > r["tgl_selesai"])
        r["dp_kecil"] = 0 < r["dibayar"] < r["total"] * 0.5 and r["total"] > 0
        r["bahan_siap"] = 1 if r["bahan_siap"] is None else r["bahan_siap"]
    return rows

def umur_ukuran(tgl):
    h = (date.today() - date.fromisoformat(tgl)).days
    return (":green[●] Pakai ulang", h) if h <= 90 else (":orange[●] Cek ulang", h) if h <= 365 else (":red[●] Ukur ulang", h)

def terakhir(pid):
    d = {}
    for u in q("SELECT * FROM ukuran WHERE pelanggan_id=? AND diperiksa IN (0,1) ORDER BY id", (pid,)): d[u["jenis"]] = json.loads(u["data"])
    return d

def form_ukuran(key, lama=None):
    """Form ukuran (cm) + validasi; selisih besar dari ukuran lama harus dikonfirmasi."""
    with st.form(key):
        jenis = st.selectbox("Jenis pakaian", PAKAIAN)
        cols = st.columns(3); data = {}
        for i, k in enumerate(UKURAN): data[k] = cols[i % 3].number_input(f"{k} (cm)", 0.0, 300.0, 0.0, 0.5)
        yakin = st.checkbox("Saya sudah cek ulang angka di atas (khusus jika berbeda jauh dari ukuran lama)")
        if st.form_submit_button("Simpan ukuran", type="primary"):
            salah = [k for k, v in data.items() if v and not 5 <= v <= 250]   # kolom 0 = tidak diisi
            sel = [f"{k}: {data[k]:g} vs lama {v:g}" for k, v in (lama or {}).get(jenis, {}).items() if k in data and data[k] and abs(data[k] - v) > LONJAKAN]
            if not any(data.values()): st.error("Isi minimal satu ukuran (cm).")
            elif salah: st.error("Ukuran tidak masuk akal (5-250 cm): " + ", ".join(salah))
            elif sel and not yakin: st.warning("Selisih > %d cm dari ukuran lama (%s). Cek ulang lalu centang konfirmasi." % (LONJAKAN, "; ".join(sel)))
            else: return jenis, {k: v for k, v in data.items() if v}
    return None

def nota(p, kunci=""):
    byr = q("SELECT * FROM bayar WHERE pesanan_id=? ORDER BY tgl", (p["id"],))
    baris = "".join(f"<tr><td>{b['tgl']}</td><td>{b['tipe']}</td><td align=right>{rp(b['jumlah'])}</td></tr>" for b in byr)
    lunas = "<b>LUNAS</b> - nota akhir, terima kasih" if p["sisa"] <= 0 else f"Sisa tagihan: <b>{rp(p['sisa'])}</b>"
    st.markdown(f"""<div class="nota"><div class="kop"><i class="lgi"></i><div><b>Jahitin ID</b><br><small>Custom made for you</small></div></div><h4>Nota #{p['id']:04d}</h4>Pelanggan: <b>{p['pelanggan']}</b><br>
    {p['jenis']} - selesai {p['tgl_selesai']} ({p['status']})<br>Total: <b>{rp(p['total'])}</b><table width=100%>{baris}</table>{lunas}</div>""", unsafe_allow_html=True)
    teks = f"JAHITIN ID - Custom made for you\nNOTA #{p['id']:04d}\n{p['pelanggan']} - {p['jenis']}\nSelesai: {p['tgl_selesai']}\nTotal: {rp(p['total'])}\n" + \
           "".join(f"{b['tgl']} {b['tipe']}: {rp(b['jumlah'])}\n" for b in byr) + f"Sisa: {rp(max(p['sisa'], 0))}"
    st.download_button("Unduh nota", teks, f"nota_{p['id']:04d}.txt", key=f"dl{kunci}{p['id']}")


# ---------- Login / Daftar ----------
def halaman_login():

    # Header utama
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

        .stApp {
            font-family: 'DM Sans', sans-serif;
        }

        .login-hero {
            background: linear-gradient(135deg, #064E3B, #047857);
            padding: 35px 25px;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 25px;
            border-bottom: 3px solid #C5A45D;
        }

        .login-hero h1 {
            font-family: 'Cormorant Garamond', serif;
            font-size: 48px;
            font-weight: 700;
            color: #FFFFFF;
            margin: 0;
        }

        .login-hero p {
            color: #E8E2D2;
            font-size: 14px;
            letter-spacing: 2px;
            margin: 3px 0 8px;
        }

        .login-hero small {
            color: #D6E5DC;
            font-size: 12px;
        }

        .login-feature {
            background: #FFFFFF;
            border: 1px solid #E5E8E1;
            border-left: 3px solid #C5A45D;
            border-radius: 10px;
            padding: 17px 15px;
            min-height: 105px;
        }

        .login-feature .number {
            font-family: 'Cormorant Garamond', serif;
            font-size: 25px;
            color: #C5A45D;
            font-weight: 700;
        }

        .login-feature b {
            color: #064E3B;
            font-size: 13px;
        }

        .login-feature small {
            color: #718078;
            font-size: 11px;
            line-height: 1.5;
        }

        div[data-testid="stTabs"] button {
            font-family: 'DM Sans', sans-serif;
            font-size: 13px;
            font-weight: 600;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #047857;
        }

        div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
            background-color: #C5A45D;
        }

        div[data-testid="stForm"] {
            background: #FFFFFF;
            border: 1px solid #E5E8E1;
            border-radius: 13px;
            padding: 24px;
        }

        .login-caption {
            text-align: center;
            color: #718078;
            font-size: 12px;
            margin-top: 12px;
        }

        </style>
    """, unsafe_allow_html=True)

    # Hero
    st.markdown(f"""
        <div class="login-hero">
            <h1>Jahitin ID</h1>
            <p>CUSTOM MADE FOR YOU</p>
            <small>Aplikasi pencatatan usaha jahit rumahan · {tgl_id()}</small>
        </div>
    """, unsafe_allow_html=True)

    tampil_flash()

    # Fitur aplikasi
    fitur = [
        ("01", "Data pelanggan terpusat",
         "Ukuran badan dan riwayat pesanan tersimpan rapi."),
        ("02", "Tenggat selalu terdeteksi",
         "Pantau tanggal selesai dan status pengerjaan."),
        ("03", "Pembayaran transparan",
         "DP, cicilan, sisa tagihan, dan nota tercatat otomatis.")
    ]

    cols = st.columns(3)

    for col, (nomor, judul, deskripsi) in zip(cols, fitur):
        col.markdown(f"""
            <div class="login-feature">
                <div class="number">{nomor}</div>
                <b>{judul}</b><br>
                <small>{deskripsi}</small>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Tab autentikasi
    t1, t2, t3 = st.tabs([
        "Masuk",
        "Daftar",
        "Lupa Password"
    ])

    # ==========================
    # MASUK
    # ==========================
    with t1:

        st.markdown("### Selamat Datang Kembali")
        st.caption("Masuk untuk melanjutkan aktivitas di Jahitin ID.")

        with st.form("login"):

            u = st.text_input(
                "Username",
                placeholder="Masukkan username atau nomor HP"
            )

            p = st.text_input(
                "Password",
                type="password",
                placeholder="Masukkan password"
            )

            masuk = st.form_submit_button(
                "Masuk ke Akun",
                type="primary",
                use_container_width=True
            )

            if masuk:

                r = q(
                    "SELECT * FROM users WHERE username=? AND pw=?",
                    (u.strip(), hp(p))
                )

                if not r:
                    st.error("Username atau password salah.")

                elif not r[0]["aktif"]:
                    st.error("Akun dinonaktifkan. Hubungi Admin.")

                else:
                    st.session_state.user = r[0]
                    catat("login")

                    nb = q(
                        "SELECT COUNT(*) n FROM notif WHERE user_id=? AND dibaca=0",
                        (r[0]["id"],)
                    )[0]["n"]

                    flash(
                        f"Selamat datang, {r[0]['nama']}!"
                        + (f" Ada {nb} notifikasi baru." if nb else "")
                    )

                    st.rerun()

        st.markdown("""
            <div class="login-caption">
                Akses demo: admin / admin123 &nbsp; | &nbsp;
                penjahit / jahit123
            </div>
        """, unsafe_allow_html=True)

    
    # ==========================
    # DAFTAR
    # ==========================
    with t2:

        st.markdown("### Buat Akun Pelanggan")
        st.caption("Daftarkan akun untuk mengakses informasi pesanan dan ukuran.")

        with st.form("daftar"):

            n = st.text_input(
                "Nama lengkap",
                placeholder="Masukkan nama lengkap"
            )

            h = st.text_input(
                "Nomor HP",
                placeholder="Contoh: 081234567890"
            )

            p = st.text_input(
                "Password",
                type="password",
                placeholder="Minimal 6 karakter"
            )

            daftar = st.form_submit_button(
                "Daftar Sekarang",
                type="primary",
                use_container_width=True
            )

        if daftar:

            ada = q(
                "SELECT * FROM users WHERE hp=?",
                (h.strip(),)
            )

            if not (
                n.strip()
                and h.strip().isdigit()
                and len(p) >= 6
            ):
                st.error(
                    "Isi nama, nomor HP berupa angka, "
                    "dan password minimal 6 karakter."
                )

            elif (
                ada
                and ada[0]["pw"] == hp("12345678")
                and ada[0]["role"] == "pelanggan"
            ):
                run(
                    "UPDATE users SET pw=?, nama=? WHERE id=?",
                    (hp(p), n.strip(), ada[0]["id"])
                )

                notif_role(
                    "penjahit",
                    f"{n.strip()} ({h.strip()}) mendaftar sendiri "
                    "dan akunnya terhubung ke data lama."
                )

                akun = q(
                    "SELECT * FROM users WHERE id=?",
                    (ada[0]["id"],)
                )

                st.session_state.user = dict(akun[0])
                st.session_state.pop("_halaman_awal", None)

                flash("Pendaftaran berhasil. Selamat datang di Jahitin ID!", "success")
                st.rerun()

            elif ada:
                st.error("Nomor HP sudah terdaftar.")

            else:
                run(
                    "INSERT INTO users(username,nama,hp,pw,role) "
                    "VALUES(?,?,?,?,'pelanggan')",
                    (h.strip(), n.strip(), h.strip(), hp(p))
                )

                notif_role(
                    "penjahit",
                    f"Pelanggan baru mendaftar sendiri: "
                    f"{n.strip()} ({h.strip()})."
                )

                akun = q(
                    "SELECT * FROM users WHERE hp=?",
                    (h.strip(),)
                )

                st.session_state.user = dict(akun[0])
                st.session_state.pop("_halaman_awal", None)

                flash("Pendaftaran berhasil. Selamat datang di Jahitin ID!", "success")
                st.rerun()

    # ==========================
    # LUPA PASSWORD
    # ==========================
    with t3:

        st.markdown("### Atur Ulang Password")
        st.caption(
            "Gunakan nomor HP dan nama lengkap yang terdaftar "
            "untuk mengatur ulang password."
        )

        with st.form("lupa"):

            h = st.text_input(
                "Nomor HP terdaftar",
                placeholder="Masukkan nomor HP"
            )

            n = st.text_input(
                "Nama lengkap",
                placeholder="Masukkan nama sesuai akun"
            )

            p = st.text_input(
                "Password baru",
                type="password",
                placeholder="Minimal 6 karakter"
            )

            reset = st.form_submit_button(
                "Atur Ulang Password",
                type="primary",
                use_container_width=True
            )

            if reset:

                r = q(
                    "SELECT * FROM users WHERE hp=? AND role='pelanggan'",
                    (h.strip(),)
                )

                if (
                    r
                    and r[0]["nama"].lower() == n.strip().lower()
                    and len(p) >= 6
                ):
                    run(
                        "UPDATE users SET pw=? WHERE id=?",
                        (hp(p), r[0]["id"])
                    )

                    st.success(
                        "Password berhasil diubah. Silakan masuk kembali."
                    )

                else:
                    st.error(
                        "Data tidak cocok atau password kurang dari "
                        "6 karakter. Jika masih gagal, minta penjahit "
                        "menghubungi Admin."
                    )

# ========================================================
# LANDING PAGE JAHITIN ID
# ========================================================
def halaman_depan():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

    .stApp {
        background: #F7F8F3;
        font-family: 'DM Sans', sans-serif;
    }

    .block-container {
        padding-top: 1.5rem;
        max-width: 1250px;
    }

    .landing-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0 22px;
        border-bottom: 1px solid #DDE5DC;
        margin-bottom: 35px;
    }

    .landing-brand {
        color: #064E3B;
        font-family: 'Playfair Display', serif;
        font-size: 27px;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .landing-brand small {
        display: block;
        font-family: 'DM Sans', sans-serif;
        font-size: 9px;
        letter-spacing: 4px;
        color: #B18B45;
        font-weight: 600;
    }

    .landing-tag {
        color: #B18B45;
        font-size: 10px;
        letter-spacing: 3px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .landing-title {
        color: #064E3B;
        font-family: 'Playfair Display', serif;
        font-size: clamp(38px, 5vw, 65px);
        line-height: 1.12;
        font-weight: 600;
        margin: 0 0 20px;
    }

    .landing-title span {
        color: #B18B45;
        font-style: italic;
    }

    .landing-desc {
        color: #68766D;
        font-size: 14px;
        line-height: 1.9;
        max-width: 480px;
        margin-bottom: 25px;
    }

    .landing-hero-image {
        width: 100%;
        height: 440px;
        object-fit: cover;
        border-radius: 4px;
        box-shadow: 12px 12px 0 #D8C69F;
    }

    .landing-section {
        text-align: center;
        margin-top: 90px;
        margin-bottom: 30px;
    }

    .landing-section small {
        color: #B18B45;
        letter-spacing: 4px;
        font-size: 10px;
        font-weight: 700;
    }

    .landing-section h2 {
        color: #064E3B;
        font-family: 'Playfair Display', serif;
        font-size: 37px;
        margin: 8px 0;
    }

    .landing-section p {
        color: #718078;
        font-size: 13px;
    }

    .landing-feature {
        background: #FFFFFF;
        padding: 25px 20px;
        min-height: 175px;
        border: 1px solid #E3E8E0;
        border-top: 3px solid #B18B45;
        border-radius: 5px;
    }

    .landing-feature h4 {
        color: #064E3B;
        font-family: 'Playfair Display', serif;
        font-size: 19px;
        margin: 0 0 12px;
    }

    .landing-feature p {
        color: #718078;
        font-size: 12px;
        line-height: 1.8;
    }

    .landing-collection {
        background: #FFFFFF;
        border: 1px solid #E5E8E1;
        padding-bottom: 15px;
        text-align: center;
    }

    .landing-collection img {
        width: 100%;
        height: 260px;
        object-fit: cover;
    }

    .landing-collection h4 {
        color: #064E3B;
        font-family: 'Playfair Display', serif;
        font-size: 20px;
        margin: 15px 0 5px;
    }

    .landing-collection p {
        color: #718078;
        font-size: 11px;
    }

    .landing-about {
        background: #064E3B;
        padding: 45px 35px;
        text-align: center;
        margin-top: 85px;
        border-bottom: 4px solid #C5A45D;
    }

    .landing-about h2 {
        color: #FFFFFF;
        font-family: 'Playfair Display', serif;
        font-size: 34px;
    }

    .landing-about p {
        color: #D6E5DC;
        font-size: 13px;
        line-height: 1.9;
        max-width: 720px;
        margin: auto;
    }

    .landing-footer {
        text-align: center;
        padding: 25px 10px;
        color: #718078;
        font-size: 11px;
        border-top: 1px solid #DDE5DC;
        margin-top: 45px;
    }

    div.stButton > button {
        border-radius: 3px;
        font-family: 'DM Sans', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        min-height: 45px;
    }

    div.stButton > button[kind="primary"] {
        background: #064E3B;
        border: 1px solid #064E3B;
        color: white;
    }

    div.stButton > button[kind="secondary"] {
        color: #064E3B;
        border: 1px solid #B18B45;
        background: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

    # NAVBAR
    st.markdown("""
    <div class="landing-nav">
        <div class="landing-brand">
            JAHITIN ID
            <small>CUSTOM MADE FOR YOU</small>
        </div>
        <div style="color:#064E3B;font-size:11px;letter-spacing:2px;">
            PERSONAL TAILORING MANAGEMENT
        </div>
    </div>
    """, unsafe_allow_html=True)


    # HERO
    kiri, kanan = st.columns([1.05, 1], gap="large")

    with kiri:
        st.markdown("""
        <div style="padding-top:45px;">
            <div class="landing-tag">THE ART OF PERSONAL TAILORING</div>
            <h1 class="landing-title">
                Every Stitch<br>
                Tells Your <span>Story.</span>
            </h1>
            <p class="landing-desc">
                Wujudkan busana yang mencerminkan karakter dan gaya
                personalmu. Jahitin ID membantu mengelola proses
                jahit dengan lebih praktis, teratur, dan profesional.
            </p>
        </div>
        """, unsafe_allow_html=True)

        tombol1, tombol2 = st.columns(2)

        with tombol1:
            if st.button(
                "MASUK",
                type="primary",
                use_container_width=True,
                key="landing_masuk"
            ):
                st.session_state["_halaman_awal"] = "auth"
                st.rerun()

        with tombol2:
            if st.button(
                "DAFTAR",
                type="secondary",
                use_container_width=True,
                key="landing_daftar"
            ):
                st.session_state["_halaman_awal"] = "auth"
                st.rerun()

    with kanan:
        st.image(
            "https://images.booqablecdn.com/uploads/4694379199ed425fafdccb4f3a546f67/photo/photo/8393b6b8-f616-45ff-99dc-ec80d29b0386/upload.png",
            use_container_width=True,
            caption="Ilustrasi proses jahit"
        )

            
    # KEUNGGULAN
    st.markdown("""
    <div class="landing-section">
        <small>WHY JAHITIN ID</small>
        <h2>Everything in One Place</h2>
        <p>Pengelolaan usaha jahit yang lebih mudah dan terorganisir.</p>
    </div>
    """, unsafe_allow_html=True)

    fitur = st.columns(4)

    daftar_fitur = [
        ("01", "Data Pelanggan", "Simpan informasi pelanggan dan ukuran dalam satu sistem."),
        ("02", "Kelola Pesanan", "Pantau setiap pesanan dan progres pengerjaan jahitan."),
        ("03", "Pembayaran", "Catat transaksi dan pantau tagihan pelanggan."),
        ("04", "Laporan Usaha", "Lihat ringkasan aktivitas dan perkembangan usaha.")
    ]

    for kolom, (nomor, nama, deskripsi) in zip(fitur, daftar_fitur):
        with kolom:
            st.markdown(f"""
            <div class="landing-feature">
                <div style="color:#B18B45;font-family:'Playfair Display';
                            font-size:25px;font-weight:700;">{nomor}</div>
                <h4>{nama}</h4>
                <p>{deskripsi}</p>
            </div>
            """, unsafe_allow_html=True)

    
    # KATALOG
    st.markdown("""
    <style>
    .katalog-card {
        width: 100%;
        height: 320px;
        overflow: hidden;
        border-radius: 14px;
        background: #F2F0E8;
    }

    .katalog-card img {
        width: 100%;
        height: 320px;
        object-fit: cover;
        display: block;
    }

    .landing-collection {
        padding: 12px 4px 18px 4px;
    }

    .landing-collection h4 {
        color: #064E3B;
        margin-bottom: 5px;
    }

    .landing-collection p {
        color: #777;
        font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="landing-section">
        <small>OUR COLLECTION</small>
        <h2>Koleksi Jahitan</h2>
        <p>Inspirasi busana untuk berbagai kebutuhan dan momen spesial.</p>
    </div>
    """, unsafe_allow_html=True)

    katalog = [
        (
            "Kebaya",
            "Elegan untuk momen istimewa.",
            "https://images.booqablecdn.com/uploads/4694379199ed425fafdccb4f3a546f67/photo/photo/50a05621-0f40-4760-bacd-45301b3be1af/Bludru_Hijau_Pradevina1.jpeg"
        ),
        (
            "Dress",
            "Tampilan anggun dan modern.",
            "https://images.booqablecdn.com/uploads/4694379199ed425fafdccb4f3a546f67/photo/photo/748e6b9d-040b-4a42-b11c-769df1dae318/Hijau_Judis2.jpeg"
        ),
        (
            "Setelan Formal",
            "Rapi untuk setiap kesempatan.",
            "https://cdn.idntimes.com/content-images/post/20240507/dewandra-1715075840016-e875fc1c1091a7453f6ce348ac0967f8.jpeg"
        )
    ]

    kolom_katalog = st.columns(3, gap="medium")

    for kolom, (nama, deskripsi, gambar) in zip(kolom_katalog, katalog):
        with kolom:
            st.markdown(
                f"""
                <div class="katalog-card">
                    <img src="{gambar}" alt="{nama}">
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(f"""
            <div class="landing-collection">
                <h4>{nama}</h4>
                <p>{deskripsi}</p>
            </div>
            """, unsafe_allow_html=True)

    # ABOUT

    # FOOTER
    st.markdown("""
    <div class="landing-footer">
        <b style="color:#064E3B;letter-spacing:2px;">JAHITIN ID</b><br>
        CUSTOM MADE FOR YOU<br><br>
        © 2026 Jahitin ID. All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)


# ---------- Penjahit ----------
def penjahit():
    m = menu(
        [
            "Ringkasan", "Papan Kerja", "Dashboard",
            "Pelanggan & Ukuran", "Pesanan",
            "Pembayaran & Nota", "Belum Lunas",
            "Lapor ke Admin", "Akun Saya"
        ],
        {
            "Ringkasan": "home",
            "Papan Kerja": "view_kanban",
            "Dashboard": "dashboard",
            "Pelanggan & Ukuran": "group",
            "Pesanan": "shopping_cart",
            "Pembayaran & Nota": "payments",
            "Belum Lunas": "receipt_long",
            "Lapor ke Admin": "campaign",
            "Akun Saya": "lock"
        }
    )

    ps = pesanan_lengkap()
    judul(m)

    if m == "Akun Saya":
        return halaman_akun()

    # ======================================================
    # 1. RINGKASAN
    # ======================================================
    if m == "Ringkasan":
        aktif = [p for p in ps if p["aktif"]]
        masuk = q("SELECT 1 FROM ukuran WHERE diperiksa=0")

        metrik([
            M("Pesanan aktif", ang(len(aktif)) + f" / {KAPASITAS}", DENIM, "keranjang",
              f"Kapasitas terpakai {len(aktif) * 100 // KAPASITAS}%"),
            M("Ukuran masuk", ang(len(masuk)), TOSCA, "ukur", "Menunggu diperiksa"),
            M("Sisa tagihan", rp(sum(p["sisa"] for p in ps if p["sisa"] > 0 and p["status"] != "Dibatalkan")), KUNING, "uang", "Belum dibayar pelanggan"),
            M("Mendesak (<=3 hari)", ang(sum(p["mendesak"] for p in ps)), MARUN, "jam", "Segera dikerjakan")
        ])

        bar(
            "Kapasitas terpakai",
            len(aktif) * 100 // KAPASITAS,
            MARUN if len(aktif) >= KAPASITAS * .8 else TOSCA
        )

        grafik_pemasukan()
        st.subheader("Pengingat")

        if len(aktif) >= KAPASITAS:
            st.error(f"Kapasitas penuh ({len(aktif)} pesanan aktif). Pertimbangkan menolak atau mengoper pesanan baru.")

        if masuk:
            st.warning(f"{len(masuk)} ukuran dari pelanggan menunggu diperiksa.")

        for p in ps:
            if p["mendesak"]:
                st.error(
                    f"{p['pelanggan']} - {p['jenis']}: "
                    f"{'TERLAMBAT' if p['hari'] < 0 else str(p['hari']) + ' hari lagi'}"
                    + (" | bahan (benang/kancing/dll) belum siap!" if not p["bahan_siap"] else "")
                )
            elif p["proses"] and not p["bahan_siap"]:
                st.warning(
                    f"{p['pelanggan']} - {p['jenis']}: bahan belum siap, "
                    f"tenggat {p['hari']} hari lagi."
                )

            if p["status"] == "Siap diambil" and p["sisa"] > 0:
                st.info(f"{p['pelanggan']} siap diambil, tagihan {rp(p['sisa'])}")

        st.subheader("Antrian pengerjaan")
        st.caption("Urutan: tanggal janji terdekat dulu, lalu yang sudah DP.")

        urut = sorted(
            [p for p in aktif if p["proses"]],
            key=lambda p: (p["tgl_selesai"], p["dibayar"] == 0)
        )

        for i, p in enumerate(urut, 1):
            st.markdown(
                f'<div class="kartu" style="animation-delay:{i * .06}s">'
                f'<b>{i}. {p["pelanggan"]}</b> - {p["jenis"]} · '
                f'janji {p["tgl_selesai"]} · {p["status"]} · '
                f'{"sudah DP" if p["dibayar"] else "belum DP"} · '
                f'{"bahan siap" if p["bahan_siap"] else "bahan belum siap"}'
                f'</div>',
                unsafe_allow_html=True
            )

        if not urut:
            st.caption("Tidak ada pesanan dalam pengerjaan.")

    # ======================================================
    # 2. PAPAN KERJA
    # ======================================================
    elif m == "Papan Kerja":
        st.caption(
            "Klik tombol untuk memindahkan pesanan ke tahap berikutnya. "
            "Pelanggan otomatis mendapat notifikasi, dan saat Siap diambil "
            "Anda bisa langsung menghubunginya lewat WhatsApp."
        )

        kol = st.columns(5)

        for k, s in enumerate(STATUS[:5]):
            isi = sorted(
                [o for o in ps if o["status"] == s],
                key=lambda o: o["tgl_selesai"]
            )

            with kol[k]:
                st.markdown(
                    f'<div class="kol" style="--c:{WARNA_STATUS[k]}">'
                    f'<span>{s}</span><b>{len(isi)}</b></div>',
                    unsafe_allow_html=True
                )

                for o in isi:
                    with st.container(border=True):
                        st.markdown(
                            f"{':red[●]' if o['mendesak'] else ':green[●]'} "
                            f"**{o['pelanggan']}**  \n"
                            f"{o['jenis']}  \n"
                            f"janji {o['tgl_selesai']}"
                            + ("  \n:orange[bahan belum siap]" if not o["bahan_siap"] else "")
                            + (
                                f"  \n:red[sisa {rp(o['sisa'])}]"
                                if o["sisa"] > 0
                                else "  \n:green[lunas]"
                            )
                        )

                        if k < 4:
                            if st.button(
                                STATUS[k + 1],
                                key=f"kb{o['id']}",
                                icon=":material/arrow_forward:"
                            ):
                                ubah_status(o, STATUS[k + 1])
                                st.rerun()
                        else:
                            st.link_button(
                                "Hubungi via WhatsApp",
                                wa(o["pelanggan_hp"], teks_wa_siap(o)),
                                icon=":material/chat:",
                                key=f"kw{o['id']}"
                            )

                if not isi:
                    st.caption("Kosong")

        st.caption(
            "Pesanan Siap diambil menjadi Diambil otomatis saat "
            "pelunasan dicatat di menu Pembayaran & Nota."
        )

    # ======================================================
    # 3. DASHBOARD
    # ======================================================
    elif m == "Dashboard":
        sah = [p for p in ps if p["status"] in STATUS]

        telat = sum(p["telat"] for p in sah)

        dur = [
            (date.fromisoformat(p["selesai_real"]) - date.fromisoformat(p["dibuat"])).days
            for p in sah
            if p["selesai_real"] and p["dibuat"]
        ]

        ukr = {}

        for u in q(
            "SELECT pelanggan_id, MAX(tgl) tgl FROM ukuran "
            "WHERE diperiksa IN (0,1) GROUP BY pelanggan_id"
        ):
            ukr[u["pelanggan_id"]] = u["tgl"]

        lama = sum(
            1 for t in ukr.values()
            if (date.today() - date.fromisoformat(t)).days > 365
        )

        pt = telat * 100 // len(sah) if sah else 0

        metrik([
            M("Total pesanan", ang(len(sah)), DENIM, "keranjang", "Semua waktu"),
            M("% terlambat", ang(pt) + "%", MARUN, "jam", f"{telat} dari {len(sah)} pesanan"),
            M("Piutang", rp(sum(p["sisa"] for p in sah if p["sisa"] > 0)), KUNING, "uang", "Belum lunas"),
            M("Rata-rata durasi", f"{sum(dur) / len(dur):.1f} hari" if dur else "-", TOSCA, "jam", "Dari dibuat sampai selesai")
        ])

        bar("Pesanan terlambat", pt, MARUN)

        bar(
            f"Pelanggan perlu ukur ulang (>1 tahun): {lama} dari {len(ukr)}",
            lama * 100 // len(ukr) if ukr else 0,
            KUNING
        )

        bln = {}

        for p in ps:
            bulan = (p["dibuat"] or p["tgl_selesai"])[:7]
            bln[bulan] = bln.get(bulan, 0) + 1

        with st.container(border=True):
            st.markdown(
                '<div class="ctitle">Pesanan per bulan</div>',
                unsafe_allow_html=True
            )

            if bln:
                st.bar_chart(dict(sorted(bln.items())), color=MARUN, height=240)

        grafik_pemasukan()

        ditolak = sum(p["status"] in BATAL[1:] for p in ps)
        st.caption(f"Dioper / ditolak karena penuh: {ditolak} pesanan")

    # ======================================================
    # 4. PELANGGAN & UKURAN
    # ======================================================
    elif m == "Pelanggan & Ukuran":
        cari = st.text_input("Cari nama / HP")

        pel = q(
            "SELECT * FROM users WHERE role='pelanggan' "
            "AND (nama LIKE ? OR hp LIKE ?)",
            (f"%{cari}%", f"%{cari}%")
        )

        # Tambah pelanggan
        with st.expander("Tambah pelanggan"):
            with st.form("tp", clear_on_submit=True):
                n = st.text_input("Nama")
                h = st.text_input("Nomor HP")

                if st.form_submit_button("Simpan"):
                    if not (n.strip() and h.strip().isdigit()):
                        st.error("Nama dan HP (angka) wajib.")

                    elif q("SELECT 1 FROM users WHERE hp=?", (h.strip(),)):
                        st.error("Nomor HP sudah terdaftar.")

                    else:
                        run(
                            "INSERT INTO users(username,nama,hp,pw,role) "
                            "VALUES(?,?,?,?,'pelanggan')",
                            (h.strip(), n.strip(), h.strip(), hp("12345678"))
                        )

                        catat(f"tambah pelanggan {h.strip()}")

                        flash(
                            "Pelanggan tersimpan. Jika ia mendaftar sendiri "
                            "dengan No. HP ini, akunnya otomatis terhubung "
                            "ke data ini."
                        )
                        st.rerun()

        # Tampilan ketika pelanggan tidak ditemukan
        if not pel:
            if cari.strip():
                st.markdown("""
                    <div style="
                        text-align: center;
                        padding: 42px 20px;
                        background: #FAFCF9;
                        border: 1px solid #D8C9A3;
                        border-radius: 12px;
                        margin-top: 15px;
                    ">
                        <div style="
                            font-family: 'Cormorant Garamond', serif;
                            font-size: 32px;
                            font-weight: 600;
                            color: #064E3B;
                        ">
                            No Result Found
                        </div>
                        <div style="
                            width: 55px;
                            height: 2px;
                            background: #C5A45D;
                            margin: 12px auto 16px;
                        "></div>
                        <div style="
                            font-family: 'DM Sans', sans-serif;
                            font-size: 13px;
                            color: #64756B;
                            line-height: 1.7;
                        ">
                            Pelanggan yang kamu cari tidak ditemukan.
                            <br>
                            Periksa kembali nama atau nomor HP.
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            else:
                st.info(
                    "Belum ada data pelanggan. "
                    "Silakan tambahkan pelanggan terlebih dahulu."
                )

            return

        # Pilih pelanggan
        p = st.selectbox(
            "Pelanggan",
            pel,
            format_func=lambda x: f"{x['nama']} ({x['hp']})"
        )

        pp = [o for o in ps if o["pelanggan_id"] == p["id"]]

        metrik([
            M("Total pesanan", ang(len(pp)), DENIM, "keranjang", "Riwayat pelanggan ini"),
            M("Sisa tagihan", rp(sum(o["sisa"] for o in pp if o["sisa"] > 0 and o["status"] in STATUS)), KUNING, "uang", "Belum lunas"),
            M("Jenis ukuran tersimpan", ang(len(terakhir(p["id"]))), TOSCA, "ukur", "Versi terbaru")
        ])

        # Riwayat pesanan
        with st.expander(f"Riwayat pesanan ({len(pp)})", expanded=bool(pp)):
            for o in sorted(pp, key=lambda o: o["tgl_selesai"], reverse=True):
                st.markdown(
                    f'<div class="kartu"><b>#{o["id"]:04d} {o["jenis"]}</b> · '
                    f'janji {o["tgl_selesai"]} · {o["status"]} · '
                    f'total {rp(o["total"])} · '
                    f'{"LUNAS" if o["sisa"] <= 0 else "sisa " + rp(o["sisa"])}</div>',
                    unsafe_allow_html=True
                )

            if not pp:
                st.caption("Belum ada pesanan.")

        # Riwayat ukuran
        st.markdown("#### Riwayat ukuran (tiap perubahan = versi baru bertanggal)")

        for u in q(
            "SELECT * FROM ukuran WHERE pelanggan_id=? ORDER BY id DESC",
            (p["id"],)
        ):
            d = json.loads(u["data"])
            badge, hari = umur_ukuran(u["tgl"])

            tag = {
                1: "diperiksa",
                0: "diisi pelanggan, belum diperiksa",
                2: "digantikan versi baru"
            }[u["diperiksa"]]

            with st.expander(
                f"{u['jenis']} - {u['tgl']} - {tag}"
                + (f" - {badge} ({hari} hari)" if u["diperiksa"] == 1 else "")
            ):
                if u["diperiksa"] != 0:
                    st.table({k: [f"{v} cm"] for k, v in d.items()})

                else:
                    with st.form(f"cek{u['id']}"):
                        cols = st.columns(3)

                        baru = {
                            k: cols[i % 3].number_input(
                                k, 0.0, 300.0, float(v), 0.5
                            )
                            for i, (k, v) in enumerate(d.items())
                        }

                        if st.form_submit_button("Perbaiki & setujui"):
                            run(
                                "UPDATE ukuran SET diperiksa=2 WHERE id=?",
                                (u["id"],)
                            )

                            run(
                                "INSERT INTO ukuran(pelanggan_id,jenis,data,diisi_oleh,diperiksa,tgl) "
                                "VALUES(?,?,?,?,1,?)",
                                (
                                    p["id"],
                                    u["jenis"],
                                    json.dumps(baru),
                                    "penjahit",
                                    str(date.today())
                                )
                            )

                            catat(f"setujui ukuran {u['id']}")

                            notif(
                                p["id"],
                                f"Ukuran {u['jenis']} Anda sudah diperiksa penjahit"
                                + (" dan dikoreksi." if baru != d else " dan disetujui.")
                            )

                            flash(
                                f"Ukuran {u['jenis']} {p['nama']} disetujui, "
                                "pelanggan diberi tahu."
                            )
                            st.rerun()

        # Catat ukuran baru
        st.markdown("#### Catat ukuran baru")

        r = form_ukuran("ukuran_p", terakhir(p["id"]))

        if r:
            run(
                "INSERT INTO ukuran(pelanggan_id,jenis,data,diisi_oleh,diperiksa,tgl) "
                "VALUES(?,?,?,?,1,?)",
                (
                    p["id"],
                    r[0],
                    json.dumps(r[1]),
                    "penjahit",
                    str(date.today())
                )
            )

            flash("Ukuran tersimpan sebagai versi baru bertanggal.")
            st.rerun()

    
    # ======================================================
    # 5. PESANAN
    # ======================================================
    
    elif m == "Pesanan":

        pel = q(
            "SELECT * FROM users WHERE role='pelanggan' AND aktif=1"
        )

        kapasitas_penuh = sum(
            p["aktif"] for p in ps
        ) >= KAPASITAS

        if kapasitas_penuh:
            st.error(
                "Kapasitas penuh. Pesanan baru belum dapat diterima."
            )

        st.markdown("### Buat Pesanan Baru")

        # --------------------------------------------------
        # PILIHAN LAYANAN
        # --------------------------------------------------
        layanan = st.selectbox(
            "Jenis layanan",
            [
                "Jahit pakaian baru",
                "Permak potong celana",
                "Ganti resleting",
                "Permak lainnya"
            ],
            key="pesanan_layanan"
        )

        daftar_pakaian = [
            "Kemeja",
            "Baju koko",
            "Celana",
            "Gamis",
            "Kebaya",
            "Rok",
            "Seragam"
        ]

        if layanan == "Permak potong celana":
            jenis_pakaian = "Celana"

        else:
            jenis_pakaian = st.selectbox(
                "Jenis pakaian",
                daftar_pakaian,
                key="pesanan_jenis_pakaian"
            )

        # --------------------------------------------------
        # TENTUKAN UKURAN SESUAI JENIS PAKAIAN
        # --------------------------------------------------
        ukuran_atas = []
        ukuran_bawah = []

        if layanan == "Jahit pakaian baru":

            if jenis_pakaian in [
                "Kemeja", "Baju koko", "Kebaya"
            ]:
                ukuran_atas = [
                    "Lingkar dada",
                    "Lingkar pinggang",
                    "Lebar bahu",
                    "Lingkar leher",
                    "Panjang baju",
                    "Panjang lengan",
                    "Lingkar lengan"
                ]

            elif jenis_pakaian == "Gamis":
                ukuran_atas = [
                    "Lingkar dada",
                    "Lingkar pinggang",
                    "Lingkar pinggul",
                    "Lebar bahu",
                    "Panjang gamis",
                    "Panjang lengan",
                    "Lingkar lengan"
                ]

            elif jenis_pakaian == "Celana":
                ukuran_bawah = [
                    "Lingkar pinggang",
                    "Lingkar pinggul",
                    "Lingkar paha",
                    "Lingkar lutut",
                    "Panjang celana",
                    "Tinggi pesak",
                    "Lingkar bawah celana"
                ]

            elif jenis_pakaian == "Rok":
                ukuran_bawah = [
                    "Lingkar pinggang",
                    "Lingkar pinggul",
                    "Panjang rok"
                ]

            elif jenis_pakaian == "Seragam":

                ukuran_atas = [
                    "Lingkar dada",
                    "Lingkar pinggang",
                    "Lebar bahu",
                    "Lingkar leher",
                    "Panjang baju",
                    "Panjang lengan",
                    "Lingkar lengan"
                ]

                jenis_bawahan = st.selectbox(
                    "Jenis bawahan seragam",
                    ["Celana", "Rok"],
                    key="pesanan_bawahan"
                )

                if jenis_bawahan == "Celana":
                    ukuran_bawah = [
                        "Lingkar pinggul",
                        "Lingkar paha",
                        "Lingkar lutut",
                        "Panjang celana",
                        "Tinggi pesak",
                        "Lingkar bawah celana"
                    ]
                else:
                    ukuran_bawah = [
                        "Lingkar pinggul",
                        "Panjang rok"
                    ]

        # --------------------------------------------------
        # FORM PESANAN
        # --------------------------------------------------
        with st.form("po", clear_on_submit=False):

            st.markdown("#### Informasi Pelanggan")

            c = st.columns(2)

            p = c[0].selectbox(
                "Pelanggan",
                pel,
                format_func=lambda x: x["nama"]
            ) if pel else None

            tgl = c[1].date_input(
                "Tanggal janji selesai",
                date.today() + timedelta(days=7)
            )

            tot = c[0].number_input(
                "Total harga (Rp)",
                min_value=0,
                step=10000
            )

            dp = c[1].number_input(
                "DP awal (Rp) - disarankan 50%",
                min_value=0,
                step=10000
            )

            bahan = st.checkbox(
                "Bahan sudah siap (benang, kancing, resleting, kain)",
                True
            )

            # --------------------------------------------------
            # DETAIL UKURAN
            # --------------------------------------------------
            st.markdown("#### Detail Ukuran")

            detail_ukuran = []

            if layanan == "Permak potong celana":

                panjang_baru = st.number_input(
                    "Panjang celana yang diinginkan (cm)",
                    min_value=0.0,
                    step=0.5
                )

                detail_ukuran.append(
                    f"Panjang celana yang diinginkan: {panjang_baru} cm"
                )

            elif layanan == "Ganti resleting":

                lokasi_resleting = st.selectbox(
                    "Lokasi resleting",
                    [
                        "Depan celana",
                        "Belakang rok/celana",
                        "Samping pakaian",
                        "Bagian depan baju",
                        "Lainnya"
                    ]
                )

                panjang_resleting = st.number_input(
                    "Panjang resleting (cm)",
                    min_value=0.0,
                    step=0.5
                )

                detail_ukuran.extend([
                    f"Lokasi resleting: {lokasi_resleting}",
                    f"Panjang resleting: {panjang_resleting} cm"
                ])

            elif layanan == "Permak lainnya":

                bagian_permak = st.selectbox(
                    "Bagian yang ingin diperbaiki",
                    [
                        "Bagian pinggang",
                        "Bagian lengan",
                        "Bagian bahu",
                        "Bagian badan",
                        "Bagian panjang pakaian",
                        "Bagian pinggul",
                        "Lainnya"
                    ]
                )

                keterangan_permak = st.text_input(
                    "Jelaskan perubahan atau ukuran yang diinginkan"
                )

                detail_ukuran.extend([
                    f"Bagian yang diperbaiki: {bagian_permak}",
                    f"Keterangan: {keterangan_permak}"
                ])

            else:

                if ukuran_atas:
                    st.markdown("**Ukuran Bagian Atas (cm)**")

                    for nama_ukuran in ukuran_atas:
                        nilai = st.number_input(
                            nama_ukuran,
                            min_value=0.0,
                            step=0.5,
                            key=f"ukuran_atas_{nama_ukuran}"
                        )

                        detail_ukuran.append(
                            f"{nama_ukuran}: {nilai} cm"
                        )

                if ukuran_bawah:
                    st.markdown("**Ukuran Bagian Bawah (cm)**")

                    for nama_ukuran in ukuran_bawah:
                        nilai = st.number_input(
                            nama_ukuran,
                            min_value=0.0,
                            step=0.5,
                            key=f"ukuran_bawah_{nama_ukuran}"
                        )

                        detail_ukuran.append(
                            f"{nama_ukuran}: {nilai} cm"
                        )

            # --------------------------------------------------
            # CATATAN DAN FOTO
            # --------------------------------------------------
            st.markdown("#### Informasi Tambahan")

            cat = st.text_area(
                "Catatan model / kain / permintaan pelanggan"
            )

            foto = st.file_uploader(
                "Foto referensi (opsional)",
                type=["png", "jpg", "jpeg"]
            )

            simpan = st.form_submit_button(
                "Buat Pesanan",
                type="primary",
                use_container_width=True
            )

            
            # --------------------------------------------------
            # SIMPAN PESANAN
            # --------------------------------------------------
            if simpan:

                if kapasitas_penuh:
                    st.error(
                        "Kapasitas penuh. Pesanan tidak dapat disimpan."
                    )

                elif not p:
                    st.error("Pilih pelanggan terlebih dahulu.")

                elif tot <= 0:
                    st.error("Total harga harus lebih dari Rp0.")

                elif dp > tot:
                    st.error("DP tidak boleh melebihi total.")

                elif layanan == "Ganti resleting" and panjang_resleting <= 0:
                    st.error("Masukkan panjang resleting.")

                elif layanan == "Permak potong celana" and panjang_baru <= 0:
                    st.error("Masukkan panjang celana yang diinginkan.")

                else:

                    jenis_pesanan = (
                        f"{layanan} - {jenis_pakaian}"
                    )

                    catatan_lengkap = (
                        f"Layanan: {layanan}\n"
                        f"Jenis pakaian: {jenis_pakaian}\n"
                    )

                    if layanan == "Jahit pakaian baru" and jenis_pakaian == "Seragam":
                        catatan_lengkap += (
                            f"Jenis bawahan: {jenis_bawahan}\n"
                        )

                    catatan_lengkap += (
                        "\nDETAIL UKURAN / PERMAK:\n"
                        + "\n".join(detail_ukuran)
                        + "\n\nCATATAN TAMBAHAN:\n"
                        + cat
                    )

                    oid = run(
                        "INSERT INTO pesanan("
                        "pelanggan_id,jenis,catatan,tgl_selesai,"
                        "status,total,bahan_siap,dibuat,foto"
                        ") VALUES(?,?,?,?,'Baru',?,?,?,?)",
                        (
                            p["id"],
                            jenis_pesanan,
                            catatan_lengkap,
                            str(tgl),
                            tot,
                            int(bahan),
                            str(date.today()),
                            foto.getvalue() if foto else None
                        )
                    )

                    if dp > 0:
                        run(
                            "INSERT INTO bayar(pesanan_id,jumlah,tipe,tgl) "
                            "VALUES(?,?,'DP',?)",
                            (oid, dp, str(date.today()))
                        )

                    catat("buat pesanan")

                    notif(
                        p["id"],
                        f"Pesanan {jenis_pesanan} Anda diterima. "
                        f"Janji selesai {tgl}. "
                        f"Total {rp(tot)}, DP {rp(dp)}, "
                        f"sisa {rp(tot - dp)}."
                    )

                    flash(
                        f"Pesanan #{oid:04d} {p['nama']} - "
                        f"{jenis_pesanan} diterima. "
                        f"Total {rp(tot)}, DP {rp(dp)}, "
                        f"sisa {rp(tot - dp)}."
                    )

                    if 0 < dp < tot * .5:
                        flash(
                            "DP kurang dari 50% dari total "
                            "(disarankan 50%).",
                            "warning"
                        )

                    st.rerun()


        # --------------------------------------------------
        # DAFTAR PESANAN
        # --------------------------------------------------
        for o in ps:

            c = st.columns([4, 2, 2, 2])

            c[0].write(
                f"{':red[●]' if o['mendesak'] else ':green[●]'} "
                f"**{o['pelanggan']}** - {o['jenis']} "
                f"(janji {o['tgl_selesai']})"
                + ("  :orange[DP < 50%]" if o["dp_kecil"] else "")
            )

            if o["status"] in STATUS:

                s = c[1].selectbox(
                    "Status",
                    STATUS,
                    STATUS.index(o["status"]),
                    key=f"s{o['id']}",
                    label_visibility="collapsed"
                )

                if s != o["status"]:
                    ubah_status(o, s)
                    st.rerun()

                b = c[2].checkbox(
                    "Bahan siap",
                    bool(o["bahan_siap"]),
                    key=f"b{o['id']}"
                )

                if b != bool(o["bahan_siap"]):
                    run(
                        "UPDATE pesanan SET bahan_siap=? WHERE id=?",
                        (int(b), o["id"])
                    )
                    st.rerun()

                if o["aktif"]:

                    with c[3].popover("Batalkan"):

                        al = st.selectbox(
                            "Alasan",
                            BATAL,
                            key=f"al{o['id']}"
                        )

                        if st.button("Simpan", key=f"bt{o['id']}"):

                            run(
                                "UPDATE pesanan SET status=? WHERE id=?",
                                (al, o["id"])
                            )

                            catat(f"{al} pesanan {o['id']}")

                            notif(
                                o["pelanggan_id"],
                                f"Pesanan {o['jenis']} Anda: {al}."
                            )

                            flash(
                                f"Pesanan {o['pelanggan']} - "
                                f"{o['jenis']}: {al}.",
                                "warning"
                            )

                            st.rerun()

            else:
                c[1].write(f"{o['status']}")

            if o["catatan"] or o["foto"]:

                with st.expander("Detail model dan ukuran"):

                    if o["catatan"]:
                        st.text(o["catatan"])

                    if o["foto"]:
                        st.image(o["foto"], width=160)

    # ======================================================
    # 6. PEMBAYARAN & NOTA
    # ======================================================
    elif m == "Pembayaran & Nota":
        if not ps:
            st.info("Belum ada pesanan.")
            return

        opsi = sorted(
            ps,
            key=lambda x: (
                x["status"] != "Siap diambil",
                x["sisa"] <= 0,
                x["tgl_selesai"]
            )
        )

        p = st.selectbox(
            "Pesanan",
            opsi,
            index=next(
                (
                    i for i, x in enumerate(opsi)
                    if x["id"] == st.session_state.get("_pilih_bayar")
                ),
                0
            ),
            format_func=lambda x:
                f"#{x['id']} {x['pelanggan']} - {x['jenis']} "
                f"({x['status']}, "
                + ("lunas" if x["sisa"] <= 0 else f"sisa {rp(x['sisa'])}")
                + ")"
        )

        metrik([
            M("Total", rp(p["total"]), DENIM, "uang", p["status"]),
            M("Sudah dibayar", rp(p["dibayar"]), TOSCA, "uang", "DP + cicilan"),
            M(
                "Sisa tagihan",
                rp(max(p["sisa"], 0)),
                MARUN if p["sisa"] > 0 else TOSCA,
                "file",
                "LUNAS" if p["sisa"] <= 0 else "Belum lunas"
            )
        ])

        if p["sisa"] <= 0:
            st.success("Pesanan ini sudah lunas. Nota akhir ada di bawah.")

        else:
            siap = p["status"] == "Siap diambil"

            if siap:
                st.info(
                    "Pesanan siap diambil: catat pelunasan, status otomatis "
                    "menjadi Diambil dan nota akhir dibuat."
                )

            with st.form(f"by{p['id']}"):
                c = st.columns(2)

                t = c[1].selectbox(
                    "Tipe",
                    ["DP", "Cicilan", "Pelunasan"],
                    index=2 if siap else (1 if p["dibayar"] else 0)
                )

                j = c[0].number_input(
                    "Jumlah (Rp)",
                    0,
                    step=10000,
                    value=int(p["sisa"]) if siap else 0
                )

                if st.form_submit_button(
                    "Catat pelunasan & serahkan pakaian"
                    if siap else "Catat pembayaran",
                    type="primary"
                ):
                    if j <= 0 or j > p["sisa"]:
                        st.error(f"Jumlah harus 1 sampai {rp(p['sisa'])}.")

                    elif t == "Pelunasan" and j != p["sisa"]:
                        st.error(
                            f"Pelunasan harus sama dengan sisa tagihan "
                            f"({rp(p['sisa'])})."
                        )

                    else:
                        catat_bayar(p, j, t)
                        st.rerun()

        nota(pesanan_lengkap("p.id=?", (p["id"],))[0], "p")

    # ======================================================
    # 7. BELUM LUNAS
    # ======================================================
    elif m == "Belum Lunas":
        bl = [
            p for p in ps
            if p["sisa"] > 0 and p["status"] in STATUS
        ]

        metrik([
            M("Total tagihan", rp(sum(p["sisa"] for p in bl)), MARUN, "uang", "Belum lunas"),
            M("Pesanan belum lunas", ang(len(bl)), DENIM, "keranjang", "Perlu ditagih")
        ])

        for p in bl:
            c = st.columns([5, 2])

            c[0].write(
                f"**{p['pelanggan']}** - {p['jenis']}: "
                f"{rp(p['sisa'])} (status {p['status']})"
            )

            c[1].link_button(
                "Tagih via WA",
                wa(
                    p["pelanggan_hp"],
                    teks_wa_siap(p)
                    if p["status"] == "Siap diambil"
                    else (
                        f"Halo {p['pelanggan']}, pesanan {p['jenis']} "
                        f"Anda sisa pembayaran {rp(p['sisa'])}. "
                        "Terima kasih  - Jahitin ID"
                    )
                ),
                key=f"wa{p['id']}"
            )

        if not bl:
            st.success("Semua pesanan lunas")

    # ======================================================
    # 8. LAPOR KE ADMIN
    # ======================================================
    else:
        st.write(
            "Ajukan reset password / nonaktifkan akun pelanggan, "
            "atau laporkan kendala. Admin hanya mengelola akun & sistem, "
            "bukan data usaha."
        )

        me = st.session_state.user
        jn = st.selectbox("Jenis laporan", JENIS_LAPOR)

        pel = (
            q("SELECT id,nama,hp FROM users WHERE role='pelanggan' ORDER BY nama")
            if jn in JENIS_AKUN else []
        )

        if jn in JENIS_AKUN and not pel:
            st.info("Belum ada akun pelanggan.")

        with st.form("lap", clear_on_submit=True):
            tg = (
                st.selectbox(
                    "Akun pelanggan yang dimaksud",
                    pel,
                    format_func=lambda x: f"{x['nama']} ({x['hp']})"
                )
                if pel else None
            )

            t = st.text_area("Pesan / keterangan")

            if st.form_submit_button("Kirim laporan", type="primary") and t.strip():
                run(
                    "INSERT INTO laporan(dari,jenis,pesan,tgl,target,status) "
                    "VALUES(?,?,?,?,?,'Baru')",
                    (
                        me["username"],
                        jn,
                        t.strip(),
                        str(date.today()),
                        tg["id"] if tg else None
                    )
                )

                notif_role("admin", f"Laporan baru dari {me['nama']}: {jn}.")
                catat("lapor admin")

                flash(
                    "Laporan terkirim ke Admin. Balasannya akan muncul "
                    "di bawah dan di notifikasi."
                )
                st.rerun()

        st.markdown("#### Laporan saya")

        for l in q(
            "SELECT l.*, u.nama t_nama FROM laporan l "
            "LEFT JOIN users u ON u.id=l.target "
            "WHERE l.dari=? ORDER BY l.id DESC",
            (me["username"],)
        ):
            with st.expander(
                f"{':green[●]' if l['balasan'] else ':orange[●]'} "
                f"#{l['id']} {l['jenis'] or 'Umum'}"
                + (f" - {l['t_nama']}" if l["t_nama"] else "")
                + f" ({l['tgl']})"
            ):
                st.write(l["pesan"])

                if l["balasan"]:
                    st.success(
                        f"Balasan Admin ({l['tgl_balas']}): {l['balasan']}"
                    )
                else:
                    st.caption("Menunggu balasan Admin.")

        st.link_button("Hubungi Admin via WhatsApp", WA_ADMIN)


# ---------- Pelanggan ----------
def pelanggan():
    u = st.session_state.user

    m = menu(
        ["Ukuran saya", "Pesanan & Nota", "Akun Saya"],
        {
            "Ukuran saya": "straighten",
            "Pesanan & Nota": "shopping_cart",
            "Akun Saya": "lock"
        }
    )

    judul(m)

    # ======================================================
    # 1. AKUN SAYA
    # ======================================================
    if m == "Akun Saya":
        return halaman_akun()

    # Mengambil seluruh pesanan milik pelanggan yang login
    pp = pesanan_lengkap("p.pelanggan_id=?", (u["id"],))

    # ======================================================
    # 2. RINGKASAN PELANGGAN
    # ======================================================
    metrik([
        M(
            "Pesanan aktif",
            ang(sum(p["aktif"] for p in pp)),
            DENIM,
            "keranjang",
            "Sedang dikerjakan"
        ),
        M(
            "Sisa tagihan",
            rp(sum(
                p["sisa"] for p in pp
                if p["sisa"] > 0 and p["status"] in STATUS
            )),
            MARUN,
            "uang",
            "Belum lunas"
        ),
        M(
            "Jenis ukuran tersimpan",
            ang(len(terakhir(u["id"]))),
            TOSCA,
            "ukur",
            "Tidak perlu ukur ulang"
        )
    ])

    # Notifikasi pesanan siap diambil
    for o in pp:
        if o["status"] == "Siap diambil":
            st.success(
                f"{o['jenis']} Anda sudah siap diambil."
                + (
                    f" Sisa tagihan {rp(o['sisa'])}."
                    if o["sisa"] > 0
                    else " Sudah lunas."
                )
            )

    # ======================================================
    # 3. UKURAN SAYA
    # ======================================================
    if m == "Ukuran saya":

        st.info(
            "Cara mengukur: pakai pita ukur, pakaian tipis, "
            "satuan cm, jangan terlalu ditarik. "
            "Ukuran lebih dari setahun sebaiknya diperbarui."
        )

        # Form pengisian ukuran
        r = form_ukuran("ukuran_c", terakhir(u["id"]))

        if r:
            run(
                "INSERT INTO ukuran(pelanggan_id,jenis,data,diisi_oleh,diperiksa,tgl) "
                "VALUES(?,?,?,?,0,?)",
                (
                    u["id"],
                    r[0],
                    json.dumps(r[1]),
                    "pelanggan",
                    str(date.today())
                )
            )

            notif_role(
                "penjahit",
                f"Ukuran {r[0]} baru dari {u['nama']} menunggu diperiksa."
            )

            flash(
                "Ukuran terkirim, menunggu diperiksa penjahit. "
                "Hasilnya akan muncul di notifikasi."
            )

            st.rerun()

        # Riwayat ukuran pelanggan
        st.markdown("#### Riwayat ukuran")

        riwayat_ukuran = q(
            "SELECT * FROM ukuran WHERE pelanggan_id=? ORDER BY id DESC",
            (u["id"],)
        )

        if not riwayat_ukuran:
            st.caption("Belum ada riwayat ukuran. Silakan isi formulir ukuran terlebih dahulu.")

        for x in riwayat_ukuran:
            status_ukuran = (
                ":green[●] sudah diperiksa"
                if x["diperiksa"] == 1
                else ":orange[●] menunggu diperiksa"
                if x["diperiksa"] == 0
                else ":gray[●] versi lama"
            )

            with st.expander(
                f"{x['jenis']} - {x['tgl']} - {status_ukuran}"
            ):
                data_ukuran = json.loads(x["data"])
                st.table({
                    k: [f"{v} cm"]
                    for k, v in data_ukuran.items()
                })

    # ======================================================
    # 4. PESANAN & NOTA
    # ======================================================
    elif m == "Pesanan & Nota":

        st.markdown("#### Riwayat pesanan")

        if not pp:
            st.info("Belum ada pesanan.")

        for p in pp:

            if p["status"] in STATUS:
                st.markdown(
                    f"**{p['jenis']}** · janji selesai {p['tgl_selesai']}"
                )

                stepper(p["status"])

            else:
                st.caption(f"{p['jenis']} - {p['status']}")

            nota(p, "c")


# ---------- Admin ----------
def admin():
    m = menu(
        ["Akun", "Backup & Restore", "Laporan", "Log", "Akun Saya"],
        {
            "Akun": "manage_accounts",
            "Backup & Restore": "backup",
            "Laporan": "inbox",
            "Log": "history",
            "Akun Saya": "lock"
        }
    )

    judul(m)

    # ======================================================
    # 1. AKUN SAYA
    # ======================================================
    if m == "Akun Saya":
        return halaman_akun()

    # ======================================================
    # 2. RINGKASAN ADMIN
    # ======================================================
    def n1(sql, a=()):
        hasil = q(sql, a)
        return hasil[0]["n"] if hasil else 0

    metrik([
        M(
            "Akun aktif",
            ang(n1("SELECT COUNT(*) n FROM users WHERE aktif=1")),
            DENIM,
            "orang",
            "Semua peran"
        ),
        M(
            "Laporan baru",
            ang(n1("SELECT COUNT(*) n FROM laporan WHERE balasan IS NULL")),
            MARUN,
            "file",
            "Menunggu balasan"
        ),
        M(
            "File backup",
            ang(len(glob.glob("backup_*.db"))),
            TOSCA,
            "kotak",
            "Di folder aplikasi"
        ),
        M(
            "Aktivitas hari ini",
            ang(n1(
                "SELECT COUNT(*) n FROM log WHERE waktu LIKE ?",
                (str(date.today()) + "%",)
            )),
            KUNING,
            "jam",
            "Tercatat di log"
        )
    ])

    # ======================================================
    # 3. KELOLA AKUN
    # ======================================================
    if m == "Akun":

        st.markdown("#### Buat akun penjahit")

        with st.form("ap", clear_on_submit=True):
            c = st.columns(3)

            nama = c[0].text_input("Nama penjahit")
            username = c[1].text_input("Username")
            password = c[2].text_input(
                "Password awal",
                type="password"
            )

            buat = st.form_submit_button(
                "Buat akun penjahit",
                type="primary"
            )

            if buat:
                if not nama.strip() or not username.strip() or not password:
                    st.error("Lengkapi seluruh data akun terlebih dahulu.")

                elif len(password) < 6:
                    st.error("Password minimal terdiri dari 6 karakter.")

                elif q(
                    "SELECT 1 FROM users WHERE username=?",
                    (username.strip(),)
                ):
                    st.error("Username sudah digunakan.")

                else:
                    run(
                        "INSERT INTO users(username,nama,hp,pw,role) "
                        "VALUES(?,?,?,?,'penjahit')",
                        (
                            username.strip(),
                            nama.strip(),
                            username.strip(),
                            hp(password)
                        )
                    )

                    catat(f"buat akun {username.strip()}")
                    flash("Akun penjahit berhasil dibuat.")
                    st.rerun()

        st.divider()
        st.markdown("#### Daftar akun pengguna")

        daftar_akun = q(
            "SELECT * FROM users ORDER BY role, nama"
        )

        if not daftar_akun:
            st.info("Belum ada akun pengguna.")

        for a in daftar_akun:

            with st.container(border=True):
                c = st.columns([3, 2, 2, 3])

                c[0].write(
                    f"{':green[●]' if a['aktif'] else ':gray[●]'} "
                    f"**{a['nama']}**"
                )
                c[0].caption(a["username"])

                c[1].write(a["role"].capitalize())

                if a["role"] != "admin":

                    if c[2].button(
                        "Nonaktifkan" if a["aktif"] else "Aktifkan",
                        key=f"t{a['id']}"
                    ):
                        run(
                            "UPDATE users SET aktif=? WHERE id=?",
                            (
                                0 if a["aktif"] else 1,
                                a["id"]
                            )
                        )

                        catat(f"toggle {a['username']}")
                        st.rerun()

                    with c[3].popover("Reset password"):
                        password_baru = st.text_input(
                            "Password baru",
                            key=f"r{a['id']}",
                            type="password"
                        )

                        if st.button(
                            "Simpan password",
                            key=f"rs{a['id']}"
                        ):
                            if len(password_baru) < 6:
                                st.error(
                                    "Password minimal 6 karakter."
                                )
                            else:
                                run(
                                    "UPDATE users SET pw=? WHERE id=?",
                                    (hp(password_baru), a["id"])
                                )

                                catat(
                                    f"reset {a['username']}"
                                )

                                st.success(
                                    "Password berhasil diubah."
                                )

    # ======================================================
    # 4. BACKUP & RESTORE
    # ======================================================
    elif m == "Backup & Restore":

        st.markdown("#### Pengelolaan database")

        if st.session_state.get("_err_backup"):
            st.error(
                "Backup otomatis gagal: "
                + st.session_state["_err_backup"]
            )

        daftar_file_backup = daftar_backup()

        if daftar_file_backup:
            backup_terakhir = datetime.fromtimestamp(
                os.path.getmtime(daftar_file_backup[0])
            )

            st.info(
                f"Backup berkala otomatis setiap {BACKUP_HARI} hari. "
                f"Maksimal {BACKUP_MAKS} salinan terakhir disimpan.\n\n"
                f"Terakhir: {backup_terakhir:%d-%m-%Y %H:%M}\n\n"
                f"Perkiraan berikutnya: "
                f"{(backup_terakhir + timedelta(days=BACKUP_HARI)):%d-%m-%Y}"
            )
        else:
            st.info(
                "Belum tersedia file backup. "
                "Silakan buat backup pertama."
            )

        if st.button(
            "Buat backup sekarang",
            type="primary",
            icon=":material/backup:"
        ):
            nama_backup = buat_backup("manual")
            flash(f"Backup berhasil dibuat: {nama_backup}")
            st.rerun()

        st.divider()
        st.markdown("#### Pulihkan database")

        if daftar_file_backup:

            file_pilihan = st.selectbox(
                "Pilih file backup",
                daftar_file_backup,
                format_func=lambda x: (
                    f"{x} "
                    f"({datetime.fromtimestamp(os.path.getmtime(x)):%d-%m-%Y %H:%M})"
                )
            )

            konfirmasi = st.checkbox(
                "Saya memahami bahwa data saat ini akan diganti "
                "dengan data dari file backup yang dipilih."
            )

            if st.button(
                "Restore data dari backup ini",
                disabled=not konfirmasi,
                icon=":material/restore:"
            ):
                try:
                    # Membuat salinan pengaman sebelum restore
                    buat_backup("pengaman sebelum restore")

                    # Memulihkan database melalui API SQLite
                    # agar lebih aman pada Windows
                    sumber = sqlite3.connect(file_pilihan)
                    tujuan = sqlite3.connect(DB)

                    try:
                        sumber.backup(tujuan)
                    finally:
                        tujuan.close()
                        sumber.close()

                    init()

                    catat("restore " + file_pilihan)

                    notif_role(
                        "penjahit",
                        "Admin memulihkan data dari backup. "
                        "Periksa kembali data terakhir Anda."
                    )

                    flash(
                        f"Data berhasil dipulihkan dari {file_pilihan}."
                    )

                    st.rerun()

                except (sqlite3.Error, OSError) as e:
                    st.error(f"Restore gagal: {e}")

        else:
            st.warning(
                "Tidak ada file backup yang dapat dipulihkan."
            )

        st.divider()
        st.markdown("#### Unduh database")

        with open(DB, "rb") as file_database:
            st.download_button(
                "Unduh database",
                file_database.read(),
                "siapjahit.db",
                mime="application/octet-stream"
            )

    # ======================================================
    # 5. LAPORAN PENJAHIT
    # ======================================================
    elif m == "Laporan":

        st.markdown("#### Daftar laporan")

        laporan = q(
            """
            SELECT
                l.*,
                u.nama AS t_nama,
                u.hp AS t_hp
            FROM laporan l
            LEFT JOIN users u ON u.id = l.target
            ORDER BY
                (l.balasan IS NOT NULL),
                l.id DESC
            """
        )

        if not laporan:
            st.info("Belum ada laporan dari penjahit.")

        for l in laporan:

            jenis_laporan = l["jenis"] or "Umum"
            aksi = (
                bool(l["target"])
                and jenis_laporan in JENIS_AKUN
            )

            indikator = (
                ":green[●]"
                if l["balasan"]
                else ":red[●]"
            )

            identitas = (
                f" - {l['t_nama']} ({l['t_hp']})"
                if l["t_nama"]
                else ""
            )

            judul_laporan = (
                f"{indikator} #{l['id']} {jenis_laporan}"
                f"{identitas} · dari {l['dari']} ({l['tgl']})"
            )

            with st.expander(
                judul_laporan,
                expanded=not bool(l["balasan"])
            ):

                st.markdown("**Isi laporan**")
                st.write(l["pesan"])

                if l["balasan"]:

                    st.success(
                        f"Dibalas pada {l['tgl_balas']}: "
                        f"{l['balasan']}"
                    )

                else:

                    with st.form(f"bl{l['id']}"):

                        catatan = st.text_area(
                            "Catatan balasan"
                            + (" (opsional)" if aksi else ""),
                            key=f"tb{l['id']}"
                        )

                        kirim = st.form_submit_button(
                            "Jalankan aksi & kirim balasan"
                            if aksi
                            else "Kirim balasan",
                            type="primary"
                        )

                        if kirim:

                            if balas_laporan(l, catatan):
                                flash(
                                    f"Laporan #{l['id']} berhasil "
                                    "diproses dan penjahit diberi tahu."
                                )
                                st.rerun()

                            else:
                                st.error(
                                    "Tulis catatan balasan terlebih dahulu."
                                )

    # ======================================================
    # 6. LOG AKTIVITAS
    # ======================================================
    elif m == "Log":

        st.markdown("#### Riwayat aktivitas sistem")

        riwayat_log = q(
            """
            SELECT waktu, aktor, aksi
            FROM log
            ORDER BY id DESC
            LIMIT 200
            """
        )

        if riwayat_log:
            st.dataframe(
                riwayat_log,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Belum ada aktivitas yang tercatat.")



# ---------- Router ----------

# ======================================================
# 1. PENGECEKAN LOGIN
# ======================================================
if "user" not in st.session_state:

    if "_halaman_awal" not in st.session_state:
        st.session_state["_halaman_awal"] = "beranda"

    if st.session_state["_halaman_awal"] == "auth":

        kolom_kembali, ruang = st.columns([1, 5])

        with kolom_kembali:
            if st.button("Kembali ke Beranda", key="kembali_beranda"):
                st.session_state["_halaman_awal"] = "beranda"
                st.rerun()

        halaman_login()

    else:
        halaman_depan()

else:
    u = st.session_state.user

    # ==================================================
    # 2. SIDEBAR BRAND
    # ==================================================
    st.sidebar.markdown(
        """
        <div class="brand">
            <i class="lgi lg"></i>
            <div>
                <b>Jahitin ID</b>
                <small>Custom made for you</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==================================================
    # 3. TOMBOL KELUAR
    # ==================================================
    if st.sidebar.button(
        "Keluar",
        icon=":material/logout:"
    ):
        catat("logout")

        del st.session_state["user"]

        flash("Anda sudah keluar.", "info")
        st.rerun()

    # ==================================================
    # 4. NOTIFIKASI PENGGUNA
    # ==================================================
    hasil_notifikasi = q(
        """
        SELECT COUNT(*) n
        FROM notif
        WHERE user_id=? AND dibaca=0
        """,
        (u["id"],)
    )

    jumlah_notifikasi = (
        hasil_notifikasi[0]["n"]
        if hasil_notifikasi
        else 0
    )

    # ==================================================
    # 5. IDENTITAS PENGGUNA
    # ==================================================
    st.empty()

    # ==================================================
    # 6. PENGARAHAN HALAMAN BERDASARKAN ROLE
    # ==================================================
    halaman_role = {
        "penjahit": penjahit,
        "pelanggan": pelanggan,
        "admin": admin
    }

    halaman_aktif = halaman_role.get(u["role"])

    if halaman_aktif:
        halaman_aktif()
    else:
        st.error(
            "Peran akun tidak dikenali. "
            "Silakan hubungi administrator."
        )
