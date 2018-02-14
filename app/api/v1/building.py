#!/usr/bin/python
# -*- coding: utf-8 -*-

from ...models.building import BuildingModel
from ... import oauth, csrf, db
from ...schemas.building import BuildingSchema
from flask import jsonify, request, current_app
from flasgger import Schema, Swagger, SwaggerView, fields


building_schema = BuildingSchema()
buildings_schema = BuildingSchema(many=True)


class Building(SwaggerView):

    decorators = [csrf.exempt, oauth.require_oauth('building')]
    definitions = {'BuildingSchema': BuildingSchema}

    def get(self, building_id):
        """
        Get a Building By its ID.
        Get a specific Building.
        ---
        tags:
        - v1
        parameters:
        - name: access_token
          in: query
          required: 'True'
          type: 'string'
          description: "Your app's access token."
        - name: building_id
          in: path
          type: int
          required: 'true'
          default: 1
          description: Which BUILDING ID to filter?
        consumes:
        - application/json
        produces:
        - application/json
        responses:
          200:
            description: 'Success: Everything worked as expected.'
            schema:
              $ref: '#/definitions/BuildingSchema'
            examples:
              Building 1:
              - BUILDINGCITY: Boston
                BUILDINGCOUNTRY: US
                BUILDINGID: 1
                BUILDINGNAME: Building 1
                BUILDINGSTATE: MA
          400:
            description: 'Bad Request: The request was unacceptable due to wrong parameter(s).'
          401:
            description: 'Unauthorized: Inavlid access_token used.'
          402:
            description: 'Request Failed.'
          500:
            description: 'Server Error: Something went wrong on our end.'

        """

        building = BuildingModel.find_by_building_id(building_id)
        if building:
            result = building_schema.dump(building)
            return jsonify(result.data)
        return (jsonify({'message': 'Building not found.'}), 404)

    def put(self, building_id):
        """
        Update a Building By its ID.
        Update a specific Building.
        You need to pass the entire Building Structure.
        ---
        tags:
        - v1
        parameters:
        - name: access_token
          in: query
          required: 'True'
          type: 'string'
          description: "Your app's access token."
        - name: building_id
          in: path
          type: int
          required: 'true'
          default: 1
          description: Which BUILDING ID to update?
        - name: body
          in: body
          required: 'True'
          schema:
            id: BuildingSchema
            properties:
              BUILDINGNAME:
                type: string
                description: Building Name
                example: Building 1
              BUILDINGCITY:
                type: string
                description: Building City
                example: Boston
              BUILDINGSTATE:
                type: string
                description: Building State
                example: MA
              BUILDINGCOUNTRY:
                type: string
                description: Building Name
                example: US
        consumes:
        - application/json
        produces:
        - application/json
        responses:
          200:
            description: 'Success: Everything worked as expected.'
            schema:
              $ref: '#/definitions/BuildingSchema'
          400:
            description: 'Bad Request: The request was unacceptable due to wrong parameter(s).'
          401:
            description: 'Unauthorized: Inavlid access_token used.'
          402:
            description: 'Request Failed.'
          500:
            description: 'Server Error: Something went wrong on our end.'

        """

        building = BuildingModel.find_by_building_id(building_id)
        input_data = request.get_json()
        if building:
            if not input_data:
                return (jsonify({'message': 'No input data provided'}),
                        400)

            (data, errors) = building_schema.load(input_data,
                    db.session)
            dict_out = {}

            if errors:
                return (jsonify(errors), 422)

            building.BUILDINGNAME = data.BUILDINGNAME
            building.BUILDINGCITY = data.BUILDINGCITY
            building.BUILDINGSTATE = data.BUILDINGSTATE
            building.BUILDINGCOUNTRY = data.BUILDINGCOUNTRY

            db.session.commit()
            result = \
                building_schema.dump(BuildingModel.query.get(building.BUILDINGID))
            return jsonify({'message': 'Updated building %s'
                           % building_id, 'building': result})

        else:
            current_app.logger.info(input_data)
            if not input_data:
                return (jsonify({'message': 'No input data provided'}), 400)

            (data, errors) = building_schema.load(input_data, db.session)
            dict_out = {}

            if errors:
                return (jsonify(errors), 422)

            building = BuildingModel(
                BUILDINGNAME=data.BUILDINGNAME,
                BUILDINGCITY=data.BUILDINGCITY,
                BUILDINGSTATE=data.BUILDINGSTATE,
                BUILDINGCOUNTRY=data.BUILDINGCOUNTRY
                )

            db.session.add(building)
            db.session.commit()
            result = \
                building_schema.dump(BuildingModel.query.get(building.BUILDINGID))
            return jsonify({'message': 'Created new building.',
                           'building': result})

    def patch(self, building_id):
        """
        Update one or more parameters of a Building By its ID.
        Update one or more parameters of a specific Building.
        Unlike PUT, you don't have to pass the entire Building Structure.
        Just pass the parameter(s) that need to be updated.
        No parameter is required. All are optional.
        ---
        tags:
        - v1
        parameters:
        - name: access_token
          in: query
          required: 'True'
          type: 'string'
          description: "Your app's access token."
        - name: building_id
          in: path
          type: int
          required: 'true'
          default: 1
          description: Which BUILDING ID to update?
        - name: body
          in: body
          required: 'True'
          schema:
            id: BuildingSchema
            properties:
              BUILDINGNAME:
                type: string
                description: Building Name
                example: Building 2
              BUILDINGCITY:
                type: string
                description: Building City
                example: Boston
              BUILDINGSTATE:
                type: string
                description: Building State
                example: MA
              BUILDINGCOUNTRY:
                type: string
                description: Building Name
                example: US
        consumes:
        - application/json
        produces:
        - application/json
        responses:
          200:
            description: 'Success: Everything worked as expected.'
            schema:
              $ref: '#/definitions/BuildingSchema'
          400:
            description: 'Bad Request: The request was unacceptable due to wrong parameter(s).'
          401:
            description: 'Unauthorized: Inavlid access_token used.'
          402:
            description: 'Request Failed.'
          500:
            description: 'Server Error: Something went wrong on our end.'

        """

        building = BuildingModel.find_by_building_id(building_id)
        if building:
            input_data = request.get_json()
            if not input_data:
                return (jsonify({'message': 'No input data provided'}),
                        400)

            (data, errors) = building_schema.load(input_data,
                    db.session, partial=True)
            dict_out = {}

            if errors:
                return (jsonify(errors), 422)


            building.BUILDINGNAME = (data.BUILDINGNAME if data.BUILDINGNAME else building.BUILDINGNAME)
            building.BUILDINGCITY = (data.BUILDINGCITY if data.BUILDINGCITY else building.BUILDINGCITY)
            building.BUILDINGSTATE = (data.BUILDINGSTATE if data.BUILDINGSTATE else building.BUILDINGSTATE)
            building.BUILDINGCOUNTRY = (data.BUILDINGCOUNTRY if data.BUILDINGCOUNTRY else building.BUILDINGCOUNTRY)

            db.session.commit()
            result = \
                building_schema.dump(BuildingModel.query.get(building.BUILDINGID))
            return jsonify({'message': 'Updated building %s'
                           % building_id, 'building': result})
        return (jsonify({'message': 'Building not found.'}), 404)

    def delete(self, building_id):
        """
        Delete a Building By its ID.
        Delete a specific Building.
        ---
        tags:
        - v1
        parameters:
        - name: access_token
          in: query
          required: 'True'
          type: 'string'
          description: "Your app's access token."
        - name: building_id
          in: path
          type: int
          required: 'true'
          default: 1
          description: Which BUILDING ID to delete?
        consumes:
        - application/json
        produces:
        - application/json
        responses:
          204:
            description: Building deleted
          400:
            description: 'Bad Request: The request was unacceptable due to wrong parameter(s).'
          401:
            description: 'Unauthorized: Inavlid access_token used.'
          402:
            description: 'Request Failed.'
          500:
            description: 'Server Error: Something went wrong on our end.'

        """

        building = BuildingModel.find_by_building_id(building_id)
        if building:
            BuildingModel.query.filter_by(BUILDINGID=building_id).delete()
            db.session.commit()
            return (jsonify({'message': 'Building has been deleted.'}),
                    204)
        return (jsonify({'message': 'Building not found.'}), 404)


class BuildingList(SwaggerView):

    decorators = [csrf.exempt, oauth.require_oauth('buildings')]
    definitions = {'BuildingSchema': BuildingSchema}

    def get(self):
        """
        Get all the Buildings.
        Get a list of all Buildings.
        ---
        tags:
        - v1
        parameters:
        - name: access_token
          in: query
          required: 'True'
          type: 'string'
          description: "Your app's access token."
        consumes:
        - application/json
        produces:
        - application/json
        responses:
          200:
            description: 'Success: Everything worked as expected.'
            schema:
              $ref: '#/definitions/BuildingSchema'
            examples:
              - BUILDINGCITY: Manchester
                BUILDINGCOUNTRY: UK
                BUILDINGID: 13
                BUILDINGNAME: Building 2
                BUILDINGSTATE: M
              - BUILDINGCITY: Oxford
                BUILDINGCOUNTRY: UK
                BUILDINGID: 15
                BUILDINGNAME: Building 3
                BUILDINGSTATE: OX
          400:
            description: 'Bad Request: The request was unacceptable due to wrong parameter(s).'
          401:
            description: 'Unauthorized: Inavlid access_token used.'
          402:
            description: 'Request Failed.'
          500:
            description: 'Server Error: Something went wrong on our end.'
        """

        buildings = BuildingModel.query.all()
        result = buildings_schema.dump(buildings)
        return jsonify(result.data)

    @oauth.require_oauth('buildings:write')
    def post(self):
        """
        Insert a Building.
        Insert a new building.
        ---
        tags:
        - v1
        parameters:
        - name: access_token
          in: query
          required: 'True'
          type: 'string'
          description: "Your app's access token."
        - name: body
          in: body
          required: 'True'
          schema:
            id: BuildingSchema
            properties:
              BUILDINGNAME:
                type: string
                description: Building Name
                example: Building
              BUILDINGCITY:
                type: string
                description: Building City
                example: Boston
              BUILDINGSTATE:
                type: string
                description: Building State
                example: MA
              BUILDINGCOUNTRY:
                type: string
                description: Building Country
                example: US
        consumes:
        - application/json
        produces:
        - application/json
        responses:
          201:
            description: 'Success: Building has been inserted.'
            schema:
              $ref: '#/definitions/BuildingSchema'
          400:
            description: 'Bad Request: The request was unacceptable due to wrong parameter(s).'
          401:
            description: 'Unauthorized: Inavlid access_token used.'
          402:
            description: 'Request Failed.'
          500:
            description: 'Server Error: Something went wrong on our end.'

        """

        input_data = request.get_json()
        current_app.logger.info(input_data)
        if not input_data:
            return (jsonify({'message': 'No input data provided'}), 400)

        (data, errors) = building_schema.load(input_data, db.session)
        dict_out = {}

        if errors:
            return (jsonify(errors), 422)

        building = BuildingModel(
            BUILDINGNAME=data.BUILDINGNAME,
            BUILDINGCITY=data.BUILDINGCITY,
            BUILDINGSTATE=data.BUILDINGSTATE,
            BUILDINGCOUNTRY=data.BUILDINGCOUNTRY
            )

        db.session.add(building)
        db.session.commit()
        result = \
            building_schema.dump(BuildingModel.query.get(building.BUILDINGID))
        return jsonify({'message': 'Created new building.',
                       'building': result})
