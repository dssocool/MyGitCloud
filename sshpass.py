import subprocess

def sshpass(host, user, password):
    # Use plink for Windows
    ssh_command = f"plink.exe -ssh {user}@{host}"

    process = subprocess.Popen(
        ssh_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )

    # Send the password to the process
    process.stdin.write(password + '\n')
    process.stdin.flush()

    # Interact with the shell
    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    host = "your_hostname"
    user = "your_username"
    password = "your_password"

    sshpass(host, user, password)
