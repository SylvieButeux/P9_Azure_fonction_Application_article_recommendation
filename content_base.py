import os
import pickle
import pandas as pd
import numpy as np


from sklearn.metrics.pairwise import cosine_similarity


#pip
#numpy
#panda
#sklearn

#pathf='./static/IMG_TEST_MODEL/Data_in/Raw/' 
# Recupère la matrice d'embedding et base_user

#----------------------
#################################
# ContentBase_recommandation: fonction qui donne les X meilleures recommandations (nb_reco) d'articles 
#                           par rapport un article deja lu par un utilisateur (UserId)
# input UserId (int)      = numero de l'utilisateur auquel on recommande 5 articles
# input base_user(dataframe) = dataframe contenant une colonne "user_id" et une colonne "acticle_id" 
# input embeddings (numpy)= matrice de vecteur (250) par acticle
# input nb_reco (int)     = Nombre de recommandation
# output (list)           = Liste des nb_reco recommandation d'article fonction du UserID    
#################################

def ContentBase_recommandation(userID, nb_reco=5):
    print("in content Base ===========================")
    embeddings = pd.read_pickle('./data/articles_embeddings.pickle')
    embeddings = embeddings.astype(np.float32)
    df_embedding = pd.DataFrame(embeddings)
    embeddings=df_embedding.to_numpy()

    base_user=pd.read_csv('./data/base_user.csv')
    print('Utilisateur ID: ', userID)

    # liste des articles vu par l 'utilisateur
    List_act_user = base_user.loc[base_user.user_id == userID]['article_id'].to_list()
    print('Liste de tous les articles lus: ', List_act_user)

    # On sélectionne le dernier article lu comme référence
    act_user_select = List_act_user[-1]
    print('Dernier article lu par l\'utilisateur: ', act_user_select)

    # on récupère les vecteurs correspondants de la matrice d'embedding
    ref=embeddings[act_user_select]
    #print(ref)
    
    # On supprime les articles deja lu par l'utilisateur de la matrice d'embedding
    for i in List_act_user:
        Clean_embed = np.delete(embeddings, i, 0)
        #print(i)
  
    # Similarité entre le dernier article lu et tous les articles de la matrice d'embedding
    # -> resultat entre 0(aucune similarité) et 1(similaire) pour tous les articles 
    result = cosine_similarity([ref], Clean_embed)[0]
    # print("result ",result)
    
    # on récupère les 5 ids des articles les plus proches/similaires (si nb_reco=5 ) 
    ids = np.argsort(result)[::-1][0:nb_reco]
    #print("ids ", ids)

    # on récupère les scores des 5 meilleurs acticles (si nb_reco=5 ) 
    scores = np.sort(result)[::-1][0:nb_reco]

    print("  pos | act Id | Score ")
    for i in range(nb_reco):
      tmp="   "+ str(i+1) +"  | "+str(ids[i])+"  | "+str(scores[i])
      print(tmp)
              
    return ids.tolist()# , ranked_similarities.tolist()
# ----------------------
#userID = 0
#vecteur_list = ContentBase_recommandation(userID, nb_reco=5)
#print('Articles recommandés : ', vecteur_list)