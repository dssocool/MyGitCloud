import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.security.Credentials;
import org.apache.hadoop.security.token.Token;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

public class GenerateDelegationToken {
    public static void main(String[] args) throws Exception {
        // Set up the Hadoop configuration
        Configuration conf = new Configuration();
        conf.set("fs.defaultFS", "hdfs://your-namenode:8020");
        
        // Authenticate using Kerberos
        FileSystem fs = FileSystem.get(conf);
        
        // Request a delegation token
        Token<?> token = fs.getDelegationToken("user");

        // Save the token to a file
        File tokenFile = new File("/path/to/delegation_token");
        try (FileOutputStream fos = new FileOutputStream(tokenFile)) {
            Credentials creds = new Credentials();
            creds.addToken(token.getService(), token);
            creds.writeTokenStorageToStream(fos);
        }
        
        System.out.println("Delegation token saved to " + tokenFile.getAbsolutePath());
    }
}
