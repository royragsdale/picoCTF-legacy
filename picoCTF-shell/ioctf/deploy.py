import argparse

def deploy(setup, generate):
  parser = argparse.ArgumentParser(description='IOCTF challenge deployment')
  parser.add_argument('--setup', help="Install required packages", action="store_true")
  parser.add_argument('--token', type=str, help="Provide random token", default='cafebabe')
  parser.add_argument('--deploy', help="Deploy a new challenge instance", action="store_true")
  args = parser.parse_args()

  if args.setup or args.deploy:
    setup()
  if args.deploy:
    server = Server()
    generate(args.token, server)
