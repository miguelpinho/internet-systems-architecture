# internet-systems-architecture
Project for the Internet Based Systems Architecture course 2018/2019.

In this project a message exchange WebApp was developed, that allows users authenticated through the FenixID service to chat with other nearby users, and receive messages from bots assigned to their current building. An authenticated admin can access the system logs, change building configuration and create/remove bots (a simple example CLI was developed for this). Bots can send messages to the users in the building they are assigned.

This system is based on REST APIs and message queues. It is developed in python flask (server) and javascript (WebApp), and was deployed in Google App Engine for evaluation.

Authors:
- João Domingos
- Rui Livramento
- Miguel Pinho
