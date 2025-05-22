import pexpect

WL_DEVUI_ADDRESS = "0x1FFF7580"
openocd_cmd = (
    f'./openocd/bin/openocd -f interface/stlink.cfg '
    f'-f target/stm32wlx.cfg '
    f'-c "init" '
    f'-c "reset halt" '
    f'-c "mdw {WL_DEVUI_ADDRESS} 3" '
    f'-c "exit"'
)

# Run the OpenOCD command using pexpect
child = pexpect.spawn(openocd_cmd, encoding='utf-8', timeout=10)
# Wait for the command to complete
child.expect(pexpect.EOF)
# Read the full output
output = str(child.before)  # Captures the entire output
# Find the line with the memory data
lines = output.split("\r\n")
# print(lines)
for line in lines:
    if str.lower(WL_DEVUI_ADDRESS) in line:
        # Split the line into parts and extract the last 3 chunks
        parts = line.split()[1:]
        devui = parts[1] + parts[0]
        print("Device UID:", " ".join(devui[i:i+2].upper() for i in range(0, len(devui), 2)))