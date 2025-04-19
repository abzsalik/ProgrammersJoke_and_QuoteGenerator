from django.shortcuts import render
from django.views import View
import requests
from django.contrib import messages
# Create your views here.

class Home(View):
    def get(self,request):
        return render(request,'app/home.html')
    
    def post(self,request):
        url ='https://official-joke-api.appspot.com/jokes/programming/random' 
        try:
            data = requests.get(url).json() 
            setup = data[0]['setup']
            punchline = data[0]['punchline']
            return render(request,'app/home.html',{
                'line1' : setup,
                'line2' : punchline,
            })
        except:
            messages.error(request,'failed')
            return render(request,'app/home.html')

class Quote(View):
    def get(self,request):
        return render(request,'app/quote.html')
    
    def post(self,request):
        search = request.POST.get('search','') #life
        url = f"https://api.freeapi.app/api/v1/public/quotes?page=1&limit=10&query={search}"

        try:
            data = requests.get(url).json()
            check_quote = data.get('data',{}).get('data',[]) 
            if not check_quote:
                messages.warning(request, 'No quotes found. write one word for accurate search!')
                return render(request, 'app/quote.html')
            quotes = [] #list [{c:v,a:v},{},{}]
            i = 0
            while i < 5 and i < len(check_quote):
                quote = {
                    'content': check_quote[i]['content'],
                    'author': check_quote[i]['author'],
                }
                quotes.append(quote)
                i += 1

            return render(request, 'app/quote.html', {
                'quotes': quotes,
            })
                
        except requests.exceptions.RequestException as e:
            # Handle network or API errors
            messages.error(request, 'Failed to fetch data. Please try again later.')
        except ValueError as e:
            # Handle the case where no quote is found
            messages.error(request, 'Not found, try different words!')
        except Exception as e:
            # Catch other unexpected errors
            messages.error(request, f'An unexpected error occurred: {str(e)}')
        return render(request, 'app/quote.html', {
            'content': 'Not found',
            'author': 'Unknown',
        })
