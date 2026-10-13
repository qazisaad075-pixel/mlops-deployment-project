def call(String command) {
    echo "Executing Shared Library Stage Command: ${command}"
    bat command
}
