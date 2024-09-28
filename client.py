import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.security.Credentials;
import org.apache.hadoop.security.UserGroupInformation;

import java.io.FileInputStream;

public class UseDelegationToken {
    public static void main(String[] args) throws Exception {
        // Set up the Hadoop configuration
        Configuration conf = new Configuration();
        conf.set("fs.defaultFS", "hdfs://your-namenode:8020");
        
        // Load the delegation token from the file
        Credentials creds = new Credentials();
        try (FileInputStream fis = new FileInputStream("/path/to/delegation_token")) {
            creds.readTokenStorageStream(fis);
        }
        
        // Set the delegation token in the UserGroupInformation object
        UserGroupInformation.getCurrentUser().addCredentials(creds);

        // Now you can use the token for operations
        FileSystem fs = FileSystem.get(conf);
        // Perform HDFS operations here
    }
}
