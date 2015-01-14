#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Adam Marinelli'

import getpass
import json
from arcpy import mapping
import tortilla


class AGOL:
    """ A class for administering an ArcGIS Online account"""

    def __init__(self, in_username, in_password, expiration=60):
        self.agol = tortilla.wrap('https://www.arcgis.com')
        self.username = in_username
        self.password = in_password
        self.expiration = expiration
        self.token = self.gen_token()

    def gen_token(self):
        """ Returns a token given a username and password """

        param = dict(username=self.username, password=self.password, expiration=self.expiration, client='referer',
                     referer='https://www.arcgis.com', f='json')

        token = self.agol.sharing.rest.generateToken.post(params=param)
        print token.token

        if hasattr(token, 'error'):
            print token.error.message
            print token.error.details
            quit()
        else:
            return token

    def get_content(self):
        """ Returns the content items for a particular user """

        param = dict(token=self.token.token, f='json')

        items = self.agol.sharing.rest.content.users(self.username).get(params=param)

        if hasattr(items, 'error'):
            print items.error.message
            print items.error.details
            quit()
        else:
            return items

    def webmap_data(self, item_id):
        """ Returns the data for a given web map item """

        param = dict(token=self.token.token, f='json')

        data = self.agol.sharing.rest.content.items(item_id).data.get(params=param)

        if hasattr(data, 'error'):
            print data.error.message
            print data.error.details
            quit()
        else:
            return data

    def webmap_edit(self, in_username, item_id, data):
        """ Posts data for a given web map item """

        param = dict(token=self.token.token, f='json', text=data)

        success = self.agol.sharing.rest.content.users(in_username).items(item_id).update.post(params=param)

        return success.success


def json_bookmarks():
    return


def mxd_bookmarks(in_map_document, in_data_frame=None):

    mxd = mapping.MapDocument(in_map_document)
    df = mapping.ListDataFrames(mxd,)

    in_data_frame = "New Data Frame 2"

    mxd = mapping.MapDocument(r"C:\Users\AMarinelli\Desktop\Frames.mxd")
    if in_data_frame is None:
        df = mapping.ListDataFrames(mxd)[0]
    else:
        try:
            df = mapping.ListDataFrames(mxd, in_data_frame)[0]
        except IndexError as detail:
            print 'Data Frame not found:', detail
        else:
            print 'Unknown Error'

    print df.name


if __name__ == "__main__":

    # Gather inputs

    BOOKMARKS = [{"extent":{"spatialReference":{"wkid":102100},"xmax":-2050429.2553922953,"xmin":-9946068.529135762,"ymax":1287382.3514782274,"ymin":-4299247.17182725},"name":"(Initial view of Brazil)"},{"extent":{"spatialReference":{"wkid":102100},"xmax":-5294034.550672936,"xmin":-5355719.232498989,"ymax":-1759321.1589398317,"ymin":-1802966.7020906087},"name":"Brasília"},{"extent":{"spatialReference":{"wkid":102100},"xmax":-4256898.7323857825,"xmin":-4318583.414211836,"ymax":-398627.39992162236,"ymin":-442272.9430723991},"name":"Fortaleza"},{"extent":{"spatialReference":{"wkid":102100},"xmax":-4744987.376500586,"xmin":-4868356.7401529085,"ymax":-2565961.118433002,"ymin":-2653252.204734707},"name":"Rio de Janeiro"},{"extent":{"spatialReference":{"wkid":102100},"xmax":-4243923.546834383,"xmin":-4305608.228660436,"ymax":-1426151.2619019134,"ymin":-1469796.8050526904},"name":"Salvador"},{"extent":{"spatialReference":{"wkid":102100},"xmax":-5127057.86238394,"xmin":-5250427.226036263,"ymax":-2659023.2003701795,"ymin":-2746314.2866718844},"name":"São Paulo"}]

    username = 'username'
    password = 'password'
    # username = raw_input('Username: ')
    # password = getpass.getpass()

    agol = AGOL(username, password)

    # content = agol.get_content()
    # print content

    # webmap = agol.webmap_data('7ecf2d7842174e41af64caa713382076')  # Sample Server
    webmap = agol.webmap_data('7ecf2d7842174e41af64caa713382076')  # My Content
    print webmap

    if hasattr(webmap, 'bookmarks') and webmap.bookmarks:
        print "FOUND"
        webmap.bookmarks = []
        result = agol.webmap_edit(username, '7ecf2d7842174e41af64caa713382076', json.dumps(webmap))
        print result
    else:
        print "NONE"
        webmap.bookmarks = BOOKMARKS
        print json.dumps(webmap, indent=4)
        result = agol.webmap_edit(username, '7ecf2d7842174e41af64caa713382076', json.dumps(webmap))
        print result

    print "\ndone"
