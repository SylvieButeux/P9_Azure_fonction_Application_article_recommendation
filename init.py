import logging
from tracemalloc import start

import azure.functions as func

import content_base as model_cb
 
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.params.get('user_id')
    if not user_id:
        # used id non recu 
        print("user_id missing")   
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )    
         
    else:  # user id => ok           
        print(str(user_id))
        nb_recommandation =5
        # on lance le model de recommandation 
        liste_result = model_cb.ContentBase_recommandation(int(user_id),nb_recommandation)
        # print(liste_result)
        final_str="" 
        for i in range (nb_recommandation ) : # mise en forme de la reponse (str): 1232 ; 3214 ; 44993 ; 76357 ; 78533
            final_str+=str(liste_result[i]) 
            if i<nb_recommandation-1:
              final_str+=" ; "
   
        print(final_str)
        return func.HttpResponse(final_str) 
           
