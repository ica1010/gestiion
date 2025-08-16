API Reference
=============

This document describes the REST API provided by Gestiion.

Base URL
--------

All API endpoints are prefixed with ``/api/v1/``.

Authentication
--------------

Most API endpoints require authentication. Use token-based authentication:

.. code-block:: http

   Authorization: Token your_token_here

Endpoints
---------

### Authentication

.. http:post:: /api/v1/auth/login/

   Authenticate a user and get an authentication token.

   :reqheader Content-Type: application/json
   :resheader Content-Type: application/json

   **Request body**:

   .. sourcecode:: http

      {
        "username": "user@example.com",
        "password": "password123"
      }

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
        "user": {
          "id": 1,
          "email": "user@example.com",
          "first_name": "John",
          "last_name": "Doe"
        }
      }

Clients
-------

.. http:get:: /api/v1/clients/
   :synopsis: List all clients.

   :resheader Content-Type: application/json
   :status 200: Success

   **Response body**:

   .. sourcecode:: javascript

      [
        {
          "id": 1,
          "name": "Client 1",
          "email": "client1@example.com"
        }
      ]

.. http:post:: /api/v1/clients/
   :synopsis: Create a new client.

   :reqheader Content-Type: application/json
   :resheader Content-Type: application/json
   :status 201: Client created
   :status 400: Invalid input data

   **Request body**:

   .. sourcecode:: javascript

      {
        "name": "New Client",
        "email": "new@example.com"
      }

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 201 Created
      Content-Type: application/json
      Location: /api/v1/clients/2/

      {
        "id": 2,
        "name": "New Client",
        "email": "new@example.com"
      }

.. http:get:: /api/v1/clients/:id/
   :synopsis: Retrieve a specific client.

   :param id: Client ID
   :type id: int
   :resheader Content-Type: application/json
   :status 200: Success
   :status 404: Client not found

   **Response body**:

   .. sourcecode:: javascript

      {
        "id": 1,
        "name": "Client 1",
        "email": "client1@example.com"
      }

.. http:put:: /api/v1/clients/:id/
   :synopsis: Update a client.

   :param id: Client ID
   :type id: int
   :reqheader Content-Type: application/json
   :resheader Content-Type: application/json
   :status 200: Client updated
   :status 400: Invalid input data
   :status 404: Client not found

   **Request body**:

   .. sourcecode:: javascript

      {
        "name": "Updated Client"
      }

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "id": 1,
        "name": "Updated Client",
        "email": "client1@example.com"
      }

.. http:delete:: /api/v1/clients/:id/
   :synopsis: Delete a client.

   :param id: Client ID
   :type id: int
   :status 204: Client deleted
   :status 404: Client not found

   **Response**:

   .. sourcecode:: http

      HTTP/1.1 204 No Content

Projects
--------

.. http:get:: /api/v1/projects/
   :synopsis: List all projects.

   :resheader Content-Type: application/json
   :status 200: Success

.. http:post:: /api/v1/projects/
   :synopsis: Create a new project.

   :reqheader Content-Type: application/json
   :resheader Content-Type: application/json
   :status 201: Project created
   :status 400: Invalid input data

.. http:get:: /api/v1/projects/:id/
   :synopsis: Retrieve a specific project.

   :param id: Project ID
   :type id: int
   :resheader Content-Type: application/json
   :status 200: Success
   :status 404: Project not found

Time Entries
------------

.. http:get:: /api/v1/time-entries/
   :synopsis: List all time entries.

   :resheader Content-Type: application/json
   :status 200: Success

.. http:post:: /api/v1/time-entries/
   :synopsis: Create a new time entry.

   :reqheader Content-Type: application/json
   :resheader Content-Type: application/json
   :status 201: Time entry created
   :status 400: Invalid input data

Invoices
--------

.. http:get:: /api/v1/invoices/
   :synopsis: List all invoices.

   :resheader Content-Type: application/json
   :status 200: Success

.. http:post:: /api/v1/invoices/
   :synopsis: Create a new invoice.

   :reqheader Content-Type: application/json
   :resheader Content-Type: application/json
   :status 201: Invoice created
   :status 400: Invalid input data

.. http:get:: /api/v1/invoices/:id/pdf/
   :synopsis: Generate PDF for an invoice.

   :param id: Invoice ID
   :type id: int
   :resheader Content-Type: application/pdf
   :status 200: PDF generated
   :status 404: Invoice not found

Error Responses
---------------

All API endpoints return standard HTTP status codes. In case of an error, the response body will contain a JSON object with an ``error`` field describing the issue.

Example error response (400 Bad Request):

.. sourcecode:: json

   {
     "error": "Invalid input data",
     "details": {
       "email": ["This field is required."]
     }
   }
