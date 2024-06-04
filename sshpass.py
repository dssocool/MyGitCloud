[PROD Cluster]             [COB Cluster]
    |                           |
    |                           |
Metastore DB                    |
    |                           |
    |---- Replication ------> Metastore_mirror DB
                                |
                                |
                                |---- Replication ------> Metastore DB
                                |
