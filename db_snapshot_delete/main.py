import boto3
from datetime import datetime, timezone

current_date = datetime.now(timezone.utc)
#print(current_date)
 
client = boto3.client('rds')
paginator = client.get_paginator('describe_db_snapshots')
for db in paginator.paginate():

    #print(db)
    for snaps in db["DBSnapshots"]:
      
      #print(snaps)
      db_snap_name = snaps['DBSnapshotIdentifier']
      print(db_snap_name)
      snapdate = snaps['SnapshotCreateTime']

      days_created= (current_date - snapdate).days
      if days_created > 400:
        print('this db_snapshot show be deleted:  ', db_snap_name)
        #client.delete_db_snapshot(DBSnapshotIdentifier=db_snap_name)

      
         
