import json
import os
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v6_0.work_item_tracking import Wiql

class DevOpsAdapter():
    """
    TODO
    """
    def __init__(self):
        config_dict = json.load(open(os.getcwd()+r"/devops_tasks/config.json"))
        self.url = 'https://dev.azure.com/'
        self.credentials = BasicAuthentication("", config_dict["personal_access_token"])
        org_dict = config_dict["org_dict"]
        states = config_dict["states"]
        self.get_work_items(org_dict, states)

    def get_work_items(self, org_dict, states):
        """
        TODO
        """
        work_item_dict = {}
        for org in org_dict:
            full_url = self.url+org
            connection = Connection(base_url=full_url,
                                    creds=self.credentials)
            try:
                wit_client = connection.clients.get_work_item_tracking_client()
            except:
                print(f"Unable to connect to: {full_url} -> [WARNING]")
                continue
            
            for state in states:
                if state not in work_item_dict.keys():
                    work_item_dict[state] = []
                work_item_dict[state].extend(self.query_boards(wit_client, self.query_parser(state)))

        for state in work_item_dict.keys():
            print("")
            print(state)
            for work_item in work_item_dict[state]:
                print(work_item)

    def query_parser(self, state):
        return """SELECT [State], [Title] 
                  FROM WorkItems
                  WHERE ([Work Item Type] = 'User Story'
                  OR [Work Item Type] = 'Bug')
                  AND ([State] =  '"""+state+"""')
                  AND [Assigned to] = @Me
                  ORDER BY [State] Asc, [Changed Date] Desc"""

    def bundle_tasks_as_list(self,work_items):
        """
        TODO
        """
        work_item_list = []
        for work_item in work_items:
            work_item_str = "[{3}] {0} {1}: {2}".format(
                             work_item.fields["System.WorkItemType"],
                             work_item.id,
                             work_item.fields["System.Title"],
                             work_item.fields["System.AreaPath"])
            work_item_list.append(work_item_str)

        return work_item_list

    def query_boards(self, wit_client, query):
        """
        TODO
        """
        query_wiql = Wiql(query=query)
        results = wit_client.query_by_wiql(query_wiql).work_items
        work_items = (wit_client.get_work_item(int(result.id)) for result in results)
        return self.bundle_tasks_as_list(work_items)