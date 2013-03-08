Releases
========

.. py2rst::

  import north
  v = north.__version__
  v = v.replace('+','')
  if v.endswith('pre'):
      print "The :doc:`%s` is in pre-release state." % v[:-3]
  else:
      print "The current stable release is :doc:`%s`." % v 
      print "We're currently working on :doc:`coming`."
  

.. toctree::
   :maxdepth: 1
   :hidden:

   coming


Older releases
--------------

.. toctree::
   :maxdepth: 1
   :glob:

   0.0.?



