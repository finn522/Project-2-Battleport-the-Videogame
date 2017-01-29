# Copyright 2017
# Simon de Bakker, Raoul van Duivenvoorde, Jeroen de Schepper

import psycopg2

def database_connection (query):
    connection = psycopg2.connect("dbname=Battleport user=postgres")

def get_highscore():
    database_connection ("SELECT * FROM highscore")

def update_score(Name):
    database_connection ("UPDATE highscore SET player_win = player_win + 1 WHERE player_name = '{}'".format(Name))