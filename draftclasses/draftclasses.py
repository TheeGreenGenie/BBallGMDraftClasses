import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rating_system.award_data import ALL_NBA, ALL_DEFENSE



draft_loading_years = ['2026']

# Players exempt from all caps — guaranteed floor of 70
OVR_CAP_EXEMPT = {
    'lebron james',
    'kobe bryant',
    'michael jordan',
    'victor wembanyama',
}

# Build sets of srIDs from award data
ALL_NBA_IDS = set()
for _season_data in ALL_NBA.values():
    for _players in _season_data.values():
        ALL_NBA_IDS.update(_players)

ALL_DEF_IDS = set()
for _season_data in ALL_DEFENSE.values():
    for _players in _season_data.values():
        ALL_DEF_IDS.update(_players)

# All-Star players by name — floor of 50 at draft
ALL_STAR_NAMES = {
    'lebron james', 'kareem abdul-jabbar', 'kobe bryant', 'kevin durant',
    'julius erving', 'tim duncan', 'kevin garnett', "shaquille o'neal",
    'michael jordan', 'karl malone', 'dirk nowitzki', 'jerry west',
    'wilt chamberlain', 'bob cousy', 'john havlicek', 'moses malone',
    'dwyane wade', 'rick barry', 'larry bird', 'stephen curry',
    'george gervin', 'elvin hayes', 'magic johnson', 'hakeem olajuwon',
    'chris paul', 'oscar robertson', 'bill russell', 'dolph schayes',
    'isiah thomas', 'charles barkley', 'elgin baylor', 'chris bosh',
    'patrick ewing', 'artis gilmore', 'james harden', 'allen iverson',
    'bob pettit', 'ray allen', 'giannis antetokounmpo', 'carmelo anthony',
    'paul arizin', 'anthony davis', 'clyde drexler', 'hal greer',
    'jason kidd', 'paul pierce', 'david robinson', 'john stockton',
    'paul george', 'kyrie irving', 'damian lillard', 'robert parish',
    'gary payton', 'russell westbrook', 'lenny wilkens', 'dominique wilkins',
    'vince carter', 'dave cowens', 'dave debusschere', 'alex english',
    'larry foust', 'dwight howard', 'nikola jokić', 'bob lanier',
    'yao ming', 'dikembe mutombo', 'steve nash', 'bill sharman',
    'lamarcus aldridge', 'dave bing', 'louie dampier', 'mel daniels',
    'joel embiid', 'walt frazier', 'harry gallatin', 'grant hill',
    'dan issel', 'joe johnson', 'kawhi leonard', 'jerry lucas',
    'ed macauley', 'slater martin', 'tracy mcgrady', 'dick mcguire',
    'kevin mchale', 'donovan mitchell', 'alonzo mourning', 'scottie pippen',
    'willis reed', 'jack sikma', 'nate thurmond', 'chet walker',
    'jo jo white', 'james worthy', 'tiny archibald', 'jimmy butler',
    'larry costello', 'adrian dantley', 'walter davis', 'demar derozan',
    'luka dončić', 'joe dumars', 'pau gasol', 'blake griffin',
    'richie guerin', 'cliff hagan', 'connie hawkins', 'tom heinsohn',
    'bailey howell', 'lou hudson', 'neil johnston', 'jimmy jones',
    'shawn kemp', 'kyle lowry', 'george mcginnis', 'vern mikkelsen',
    "jermaine o'neal", 'tony parker', 'mitch richmond', "amar'e stoudemire",
    'jayson tatum', 'karl-anthony towns', 'jack twyman', 'george yardley',
    'zelmo beaty', 'chauncey billups', 'devin booker', 'carl braun',
    'jaylen brown', 'mack calvin', 'billy cunningham', 'brad daugherty',
    'wayne embry', 'donnie freeman', 'tom gola', 'gail goodrich',
    'tim hardaway', 'spencer haywood', 'al horford', 'dennis johnson',
    'gus johnson', 'marques johnson', 'bobby jones', 'sam jones',
    'larry kenon', 'rudy larusso', 'kevin love', 'maurice lucas',
    'pete maravich', 'bob mcadoo', 'reggie miller', 'sidney moncrief',
    'chris mullin', 'don ohl', 'andy phillip', 'charlie scott',
    'gene shue', 'ralph simpson', 'david thompson', 'klay thompson',
    'rudy tomjanovich', 'wes unseld', 'john wall', 'bobby wanzer',
    'chris webber', 'paul westphal', 'vin baker', 'walt bellamy',
    'otis birdsong', 'rolando blackman', 'ron boone', 'roger brown',
    'joe caldwell', 'tom chambers', 'maurice cheeks', 'doug collins',
    'demarcus cousins', 'bob dandridge', 'bob davies', 'anthony edwards',
    'dick garmaker', 'shai gilgeous-alexander', 'draymond green', 'johnny green',
    'anfernee hardaway', 'mel hutchins', 'warren jabali', 'larry jones',
    'bernard king', 'bill laimbeer', 'clyde lovellette', 'shawn marion',
    'george mikan', 'paul millsap', 'earl monroe', 'willie naulls',
    'bob netolicky', 'billy paultz', 'jim pollard', 'mark price',
    'michael ray richardson', 'arnie risen', 'red robbins', 'alvin robertson',
    'guy rodgers', 'rajon rondo', 'ralph sampson', 'pascal siakam',
    'latrell sprewell', 'kemba walker', 'ben wallace', 'rasheed wallace',
    'sidney wicks', 'trae young', 'bam adebayo', 'mark aguirre',
    'gilbert arenas', 'bradley beal', 'john beasley', 'bill bridges',
    'larry brown', 'jalen brunson', 'darel carrier', 'phil chenier',
    'glen combs', 'terry dischinger', 'steve francis', 'marc gasol',
    'rudy gobert', 'richard hamilton', 'kevin johnson', 'stew johnson',
    'eddie jones', 'steve jones', 'bob kauffman', 'red kerr',
    'billy knight', 'freddie lewis', 'bob love', 'dan majerle',
    'bill melchionni', 'khris middleton', 'doug moe', 'jeff mullins',
    'larry nance', 'julius randle', 'glen rice', 'derrick rose',
    'dan roundfield', 'brandon roy', 'domantas sabonis', 'detlef schrempf',
    'paul seymour', 'ben simmons', 'peja stojaković', 'maurice stokes',
    'george thompson', 'dick van arsdale', 'tom van arsdale', 'norm van lier',
    'antoine walker', 'jamaal wilkes', 'buck williams', 'deron williams',
    'willie wise', 'marvin barnes', 'scottie barnes', 'leo barnhorst',
    'byron beck', 'art becker', 'carlos boozer', 'elton brand',
    'terrell brandon', 'frankie brian', 'john brisker', 'don buse',
    'caron butler', 'archie clark', 'terry cummings', 'cade cunningham',
    'baron davis', 'warren davis', 'luol deng', 'john drew',
    'andre drummond', 'kevin duckworth', 'walter dukes', 'dike eddleman',
    'sean elliott', 'michael finley', "de'aaron fox", 'joe fulks',
    'darius garland', 'jack george', 'manu ginóbili', 'tyrese haliburton',
    'roy hibbert', 'jrue holiday', 'allan houston', 'hot rod hundley',
    'les hunter', 'zydrunas ilgauskas', 'brandon ingram', 'jaren jackson jr.',
    'antawn jamison', 'eddie johnson', 'john johnson', 'larry johnson',
    'rich jones', 'don kojis', 'wendell ladner', 'zach lavine',
    'david lee', 'fat lever', 'mike lewis', 'rashard lewis',
    'jeff malone', 'danny manning', 'stephon marbury', 'jack marin',
    'tyrese maxey', 'brad miller', 'ja morant', 'swen nater',
    'norm nixon', 'joakim noah', 'victor oladipo', 'jim paxson',
    'geoff petrie', 'terry porter', 'cincy powell', 'zach randolph',
    'glenn robinson', 'truck robinson', 'red rocha', 'dennis rodman',
    'jeff ruland', 'fred scolari', 'kenny sears', 'frank selvy',
    'alperen şengün', 'james silas', 'paul silas', 'jerry sloan',
    'phil smith', 'randy smith', 'jerry stackhouse', 'levern tart',
    'brian taylor', 'reggie theus', 'isaiah thomas', 'andrew toney',
    'kelly tripucka', 'kiki vandeweghe', 'bob verga', 'nikola vučević',
    'jimmy walker', 'bill walton', 'scott wedman', 'victor wembanyama',
    'david west', 'charlie williams', 'chuck williams', 'gus williams',
    'zion williamson', 'brian winters', 'shareef abdur-rahim', 'alvan adams',
    'michael adams', 'danny ainge', 'jarrett allen', 'kenny anderson',
    'b.j. armstrong', 'deni avdija', 'lamelo ball', 'paolo banchero',
    'don barksdale', 'dick barnett', 'dana barros', 'butch beard',
    'ralph beard', 'mookie blaylock', 'john block', 'bob boozer',
    'vince boryla', 'bill bradley', 'fred brown', 'larry bunce',
    'andrew bynum', 'austin carr', 'joe barry carroll', 'george carter',
    'bill cartwright', 'sam cassell', 'cedric ceballos', 'tyson chandler',
    'len chappell', 'nat clifton', 'derrick coleman', 'jack coleman',
    'mike conley', 'antonio davis', 'dale davis', 'vlade divac',
    'james donaldson', 'goran dragić', 'jalen duren', 'jim eakins',
    'mark eaton', 'dale ellis', 'ray felix', 'sleepy floyd',
    'jimmy foster', 'world b. free', 'bill gabor', 'chris gatling',
    'gus gerard', 'gerald govan', 'danny granger', 'horace grant',
    'a.c. green', 'mike green', 'rickey green', 'alex groza',
    'tom gugliotta', 'devin harris', 'bob harrison', 'hersey hawkins',
    'gordon hayward', 'walt hazzard', 'tyler herro', 'art heyman',
    'wayne hightower', 'tyrone hill', 'lionel hollins', 'chet holmgren',
    'jeff hornacek', 'josh howard', 'juwan howard', 'andre iguodala',
    'darrall imhoff', 'luke jackson', 'mark jackson', 'merv jackson',
    'tony jackson', 'jalen johnson', 'neil johnson', 'steve johnson',
    'caldwell jones', 'wil jones', 'deandre jordan', 'chris kaman',
    'julius keye', 'jim king', 'andrei kirilenko', 'kyle korver',
    'sam lacey', 'christian laettner', 'clyde lee', 'reggie lewis',
    'goose ligon', 'brook lopez', 'jamaal magloire', 'randy mahaffey',
    'lauri markkanen', 'kenyon martin', 'jamal mashburn', 'anthony mason',
    'ted mcclain', 'xavier mcdaniel', 'jim mcdaniels', 'antonio mcdyess',
    'jon mcglocklin', 'dewitt menyard', 'tom meschery', 'eddie miles',
    'mike mitchell', 'steve mix', 'evan mobley', 'jack molinas',
    'gene moore', 'calvin murphy', 'dejounte murray', 'jamal murray',
    'calvin natt', 'jameer nelson', 'chuck noble', 'charles oakley',
    'mehmet okur', 'ricky pierce', 'kristaps porziņģis', 'norman powell',
    'jim price', 'theo ratliff', 'michael redd', 'richie regan',
    'doc rivers', 'clifford robinson', 'flynn robinson', 'curtis rowe',
    'bob rule', 'campy russell', 'cazzie russell', "d'angelo russell",
    'woody sauldsberry', 'fred schaus', 'lee shaffer', 'lonnie shelton',
    'walt simon', 'adrian smith', 'steve smith', 'rik smits',
    'willie somerset', 'john starks', 'don sunderlage', 'wally szczerbiak',
    'jeff teague', 'claude terry', 'skip thoren', 'otis thorpe',
    'monte towe', 'dave twardzik', 'nick van exel', 'fred vanvleet',
    'chico vaughn', 'gerald wallace', 'paul walther', 'ben warley',
    'kermit washington', 'trooper washington', 'andrew wiggins', 'jalen williams',
    'jayson williams', 'mo williams', 'kevin willis', 'metta world peace',
    'max zaslofsky',
}

# cap/floor tiers
CAP_ALLNBA    = 65  # All-NBA: cap 65, floor 55
FLOOR_ALLNBA  = 55
CAP_ALLDEF    = 65  # All-Defensive only: cap 65, no floor
CAP_DEFAULT   = 60  # everyone else: cap 60, no floor
FLOOR_ALLSTAR = 50  # All-Star players: floor 50 (applied on top of tier floors)

# All skill ratings (used for OVR cap scaling — hgt excluded as a physical attribute)
SKILL_RATINGS = ['stre', 'spd', 'jmp', 'endu', 'ins', 'dnk', 'ft', 'fg', 'tp', 'diq', 'oiq', 'drb', 'pss', 'reb']

# Ratings eligible for the under-cap boost (excludes high-weight attrs: spd, oiq, diq)
BOOST_RATINGS = ['stre', 'jmp', 'endu', 'ins', 'dnk', 'ft', 'fg', 'tp', 'drb', 'pss', 'reb']

BIG_POSITIONS = {'PF', 'C'}
BIG_OVR_ADJUSTMENTS = {
    'tp': 10,
    'drb': 10,
    'oiq': 1,
}


def compute_ovr(r):
    """Exact BBGM OVR formula (ovr.basketball.ts)."""
    val = (
        0.159  * (r['hgt']  - 47.5) +
        0.0777 * (r['stre'] - 50.2) +
        0.123  * (r['spd']  - 50.8) +
        0.051  * (r['jmp']  - 48.7) +
        0.0632 * (r['endu'] - 39.9) +
        0.0126 * (r['ins']  - 42.4) +
        0.0286 * (r['dnk']  - 49.5) +
        0.0202 * (r['ft']   - 47.0) +
        0.0726 * (r['tp']   - 47.1) +
        0.133  * (r['oiq']  - 46.8) +
        0.159  * (r['diq']  - 46.7) +
        0.059  * (r['drb']  - 54.8) +
        0.062  * (r['pss']  - 51.3) +
        0.01   * (r['fg']   - 47.0) +
        0.01   * (r['reb']  - 51.4) +
        48.5
    )
    if val >= 68:
        fudge = 8
    elif val >= 50:
        fudge = 4 + (val - 50) * (4 / 18)
    elif val >= 42:
        fudge = -5 + (val - 42) * (9 / 8)
    elif val >= 31:
        fudge = -5 - (42 - val) * (5 / 11)
    else:
        fudge = -10
    return round(val + fudge)


def apply_ovr_floor(ratings, floor):
    """Scale skill ratings away from midpoint (50) until OVR >= floor."""
    if compute_ovr(ratings) >= floor:
        return

    original = {k: ratings[k] for k in SKILL_RATINGS}

    lo, hi = 1.0, 3.0
    for _ in range(40):
        mid = (lo + hi) / 2
        probe = dict(ratings)
        for k in SKILL_RATINGS:
            probe[k] = max(0, min(100, round(50 + mid * (original[k] - 50))))
        if compute_ovr(probe) < floor:
            lo = mid
        else:
            hi = mid

    for k in SKILL_RATINGS:
        ratings[k] = max(0, min(100, round(50 + hi * (original[k] - 50))))


def apply_ovr_cap(ratings, cap):
    """
    Scale skill ratings toward midpoint (50) until OVR <= cap.
    hgt is left untouched. Uses binary search for precision.
    """
    if compute_ovr(ratings) <= cap:
        return

    original = {k: ratings[k] for k in SKILL_RATINGS}

    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        probe = dict(ratings)
        for k in SKILL_RATINGS:
            probe[k] = round(50 + mid * (original[k] - 50))
        if compute_ovr(probe) > cap:
            hi = mid
        else:
            lo = mid

    for k in SKILL_RATINGS:
        ratings[k] = max(0, min(100, round(50 + lo * (original[k] - 50))))


def adjust_big_ovr_bias(player):
    """
    PF/C prospects read about 2 OVR high because hgt carries so much weight.
    Pull down lower-value perimeter ratings before the normal cap/floor pass.
    """
    if player.get('pos') not in BIG_POSITIONS:
        return

    for season_ratings in player.get('ratings', []):
        for rating, delta in BIG_OVR_ADJUSTMENTS.items():
            season_ratings[rating] = max(0, season_ratings[rating] - delta)


for year in draft_loading_years:
    league_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'leagues',
        'base_leagues',
        f'league{year}.json',
    )
    with open(league_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    draftyear = data['startingSeason']-1

    draftplayers = {
        "startingSeason" : draftyear,
        "players" : []
    }

    for player in data['players']:
        try:
            playerdraftyear = player['draft']['year']
            if playerdraftyear == draftyear-1:
                player['tid'] = -2

                name_lower = player.get('name', '').lower()
                adjust_big_ovr_bias(player)
                if name_lower in OVR_CAP_EXEMPT:
                    # Exempt player — enforce minimum floor of 70
                    for season_ratings in player.get('ratings', []):
                        before = compute_ovr(season_ratings)
                        if before < 70:
                            apply_ovr_floor(season_ratings, 70)
                            after = compute_ovr(season_ratings)
                            print(f"  [FLOOR] {player['name']}: {before} -> {after}")
                else:
                    sr_id = player.get('srID', '')
                    is_allnba = sr_id in ALL_NBA_IDS
                    is_alldef = sr_id in ALL_DEF_IDS
                    is_allstar = name_lower in ALL_STAR_NAMES

                    if is_allnba:
                        cap, floor = CAP_ALLNBA, FLOOR_ALLNBA
                    elif is_alldef:
                        cap, floor = CAP_ALLDEF, None
                    else:
                        cap, floor = CAP_DEFAULT, None

                    # All-Star floor stacks on top — only raises, never lowers
                    if is_allstar and (floor is None or floor < FLOOR_ALLSTAR):
                        floor = FLOOR_ALLSTAR

                    for season_ratings in player.get('ratings', []):
                        before = compute_ovr(season_ratings)
                        if before > cap:
                            apply_ovr_cap(season_ratings, cap)
                            after = compute_ovr(season_ratings)
                            print(f"  [CAP] {player['name']}: {before} -> {after}")
                        elif floor is not None and before < floor:
                            apply_ovr_floor(season_ratings, floor)
                            after = compute_ovr(season_ratings)
                            print(f"  [FLOOR] {player['name']}: {before} -> {after}")
                        elif before < cap:
                            # Under cap — small boost to low-weight attrs only, then enforce cap
                            for k in BOOST_RATINGS:
                                season_ratings[k] = min(100, season_ratings[k] + 2)
                            apply_ovr_cap(season_ratings, cap)

                print(f"{player['name']} was added to the {playerdraftyear} draft class (ovr={compute_ovr(player['ratings'][-1])})")
                print(f"{'-'*50}")
                draftplayers['players'].append(player)
        except:
            pass

    print(f"{year}: {len(draftplayers['players'])} draft prospects")

    with open(f'{draftyear-1}draft.json', 'w') as f:
        json.dump(draftplayers, f, indent=4)
