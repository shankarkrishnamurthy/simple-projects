Description:
   run express --view ?? video-ideas-jotting-app
   modify express-handlebar as the rendering engine 
   now routes are put in the app
   route files directly call rendering view name for each route
   rendering happens in layer. 1st render 'main' for every rendering. Then follow with individual 'body' and recursively fill the '_partial' (both in main and body)
