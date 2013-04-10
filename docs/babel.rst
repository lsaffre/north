.. _mldbc:

=============================
Multilingual database content
=============================

North includes, as a side effect, a 
facility to develop application that offer 
support for multilingual database content.

For example, a Canadian company 
might want to print catalogs and price offers in an 
English and a French version, 
but don't want to maintain different product tables. 
So they need a Products table like this:

  +--------------+------------------+-------------+-------+----+
  | Designation  | Designation (fr) | Category    | Price | ID |
  +==============+==================+=============+=======+====+
  | Chair        | Chaise           | Accessories | 29.95 | 1  |
  +--------------+------------------+-------------+-------+----+
  | Table        | Table            | Accessories | 89.95 | 2  |
  +--------------+------------------+-------------+-------+----+
  | Monitor      | Écran            | Hardware    | 19.95 | 3  |
  +--------------+------------------+-------------+-------+----+
  | Mouse        | Souris           | Accessories |  2.95 | 4  |
  +--------------+------------------+-------------+-------+----+
  | Keyboard     | Clavier          | Accessories |  4.95 | 5  |
  +--------------+------------------+-------------+-------+----+

If your application is being used both in Canada and the US, 
then your US clients don't want to have a "useless" column for the 
French designation of their products.

See also:

- The :doc:`/tutorials/catalog/index` tutorial
- The :attr:`languages <djangosite.Site.languages>` setting
