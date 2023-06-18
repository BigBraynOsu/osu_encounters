from flask import Flask, request
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from models import db, Match, User
from apiv1 import apikey
from ossapi import OssapiV1
import os
import re
import tqdm
import json
from sqlalchemy import desc


bp = Blueprint('bp', __name__)

@bp.route("/")
def home():
    return "Test123"

@bp.route('/test')
def test():
    return "Test"

@bp.route('/matchpull')
def matchpull():
    match = apikey.get_match(107976982)
    dict = {}
    for game in match.games:
        for score in game.scores:
            userid = score.user_id
            user = apikey.get_user(userid)
            dict[user.username] = userid
    
    return dict

@bp.post('/addnewmatch/<matchid>')
def addmatch(matchid):
    match = apikey.get_match(matchid)
    dbmatch = Match()
    dbmatch.match_id = matchid
    db.session.add(dbmatch)
    # userset = set()
    # for game in match.games:
    #     for score in game.scores:
    #         userid = score.user_id
    #         userset.add(userid)
    
    # for userid in userset:
    #     user = User(user_id=userid)
    #     db.session.add(user)

    db.session.commit()
    return "", 204

@bp.post('/baseload')
def baseload():
    with open("multimatches.txt", "r") as file:
        for line in file:
            match = re.search(r"/(\d+)$", line)
            if match:
                matchid = int(match.group(1))
                dbmatch = Match(match_id=matchid)
                db.session.add(dbmatch)
    
    db.session.commit()
    return "", 204

@bp.route('/getallusers')
async def getallusers():
    dbmatches = Match.query.filter_by(evaluated=False)
    user_encounters = {}
    for dbmatch in tqdm.tqdm(dbmatches):
        try:
            match = apikey.get_match(dbmatch.match_id)
        except Exception:
            db.session.delete(dbmatch)
            continue

        userset = set()
        for game in match.games:
            for score in game.scores:
                userid = score.user_id
                userset.add(userid)
    
        for user_id in userset:
            user_encounters[user_id] = (user_encounters.get(user_id) or 0) + 1

        dbmatch.evaluated = True

        db.session.commit()
    
    for user_id, encounters in user_encounters.items():
        dbuser = User.query.filter_by(user_id=user_id).first()
        if not dbuser:
            dbuser = User()
            dbuser.user_id = user_id
            db.session.add(dbuser)
        dbuser.encounters = encounters

    db.session.commit()

    return user_encounters


@bp.get('/retrieve-users')
def retrieveUsers():
    limit = request.args.get('limit', default = 20, type = int)
    dbusers = User.query.filter(User.user_id!=3344333).order_by(desc(User.encounters)).limit(limit)
    userinfos = []
    for user in dbusers:
        apiuser = apikey.get_user(user.user_id)
        userinfo = {
            "user_id": apiuser.user_id,
            "username": apiuser.username,
            "rank": apiuser.rank,
            "country": apiuser.country,
            "encounters": user.encounters
        }
        userinfos.append(userinfo)
    
    return json.dumps(userinfos)
        