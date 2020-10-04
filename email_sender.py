import boto3
from botocore.exceptions import ClientError

def send_email(date, info, statistics):
  SENDER = "Covid-19 Notifier <samrolandwaters@gmail.com>"
  RECIPIENT = "samrolandwaters@gmail.com"
  AWS_REGION = "us-west-2"
  SUBJECT = f'Covid-19 Statistics for {date}'
  BODY_HTML = (
    '<html>'
      '<head></head>'
      '<body>'
        f'<h1>{SUBJECT}</h1>'
        f'{format_statistics(statistics)}'
        f'<p><i>{info}</i></p>'
      '</body>'
    '</html>'
  )
  CHARSET = "UTF-8"

  # Create new SES resource and specify a region
  client = boto3.client('ses', region_name=AWS_REGION)

  # Try to send the email
  try:
    response = client.send_email(
      Destination={
        'ToAddresses': [
          RECIPIENT,
        ],
      },
      Message={
        'Body': {
          'Html': {
            'Charset': CHARSET,
            'Data': BODY_HTML,
          },
          'Text': {
            'Charset': CHARSET,
            'Data': BODY_HTML,
          },
        },
        'Subject': {
          'Charset': CHARSET,
          'Data': SUBJECT,
        },
      },
      Source=SENDER
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])

def format_statistics(stats) -> str:
  formatted = ''
  for s in stats:
    formatted += (
      f'<h3>{s["county"]}</h3>'
      '<ul>'
        f'<li>New cases: {s["new_cases"]}</li>'
        f'<li>New deaths: {s["new_deaths"]}</li>'
        f'<li>Total cases: {s["total_cases"]}</li>'      
      '</ul>'
    )
  return formatted