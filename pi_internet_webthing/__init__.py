from pi_internet_webthing.internet_webthing import run_server
from pi_internet_webthing.app import App
from string import Template

PACKAGENAME = 'pi_internet_webthing'
ENTRY_POINT = "netmonitor"
DESCRIPTION = "A web connected local internet speed and connectivity monitor"


UNIT_TEMPLATE = Template('''
[Unit]
Description=$packagename
After=syslog.target

[Service]
Type=simple
ExecStart=$entrypoint --command listen --hostname $hostname --port $port --verbose $verbose --speedtest_period $speedtest_period --connecttest_period $connecttest_period --connecttest_url $connecttest_url
SyslogIdentifier=$packagename
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
''')



class InternetApp(App):

    def do_add_argument(self, parser):
        parser.add_argument('--speedtest_period', metavar='speedtest_period', required=False, type=int, default=0, help='the speedtest period in sec')
        parser.add_argument('--connecttest_period', metavar='connecttest_period', required=False, type=int, default=0, help='the connecttest period in sec')
        parser.add_argument('--connecttest_url', metavar='connecttest_url', required=False, type=str, default="http://google.com", help='the url to connect runnig the connect test')

    def do_additional_listen_example_params(self):
        return "--speedtest_period 900 --connecttest_period 5 --connecttest_url http://google.com"

    def do_process_command(self, command:str, hostname: str, port: int, verbose: bool, args) -> bool:
        if command == 'listen' and (args.speedtest_period > 0 or args.connecttest_period > 0):
            run_server(hostname, port, self.description, args.speedtest_period, args.connecttest_period, args.connecttest_url)
            return True
        elif args.command == 'register' and (args.speedtest_period > 0 or args.connecttest_period > 0):
            print("register " + self.packagename + " on port " + str(args.port) + " with speedtest_period " + str(args.speedtest_period) + "sec and connecttest_period " + str(args.connecttest_period) + "sec")
            unit = UNIT_TEMPLATE.substitute(packagename=self.packagename, entrypoint=self.entrypoint, hostname=hostname, port=port, verbose=verbose, speedtest_period=args.speedtest_period, connecttest_period=args.connecttest_period, connecttest_url=args.connecttest_url)
            self.unit.register(hostname, port, unit)
            return True
        else:
            return False

def main():
    InternetApp(PACKAGENAME, ENTRY_POINT, DESCRIPTION).handle_command()


if __name__ == '__main__':
    main()


