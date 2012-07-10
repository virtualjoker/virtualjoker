# cron_jobs_handler.py
#
# /cron_jobs
#
# This handler will add the server task queue


from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class CronJobsHandler(webapp.RequestHandler):
  """ CronJobsHandler
      This CronJobs will be performed in constant time,
      ensuring that the server will aways be called """
  def get(self):
    action = self.request.get('action')
    taskqueue.add(queue_name='server', url='/server', method='GET', params={'action':action})
    self.response.out.write('ACTION ENQUEUED: '+str(action))


# ----------------------------------------------------------------------- #


application = webapp.WSGIApplication(
    [
      ('/.*', CronJobsHandler)
    ],
    debug = True
  )

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
