======
Design
======

Workflow Pieces
----------------

* Apps
* Apps.models
* AdminObj
* Appstore

Workflow
----------------

1. Instantiate Appstore
2. Loop through the Apps then models per App
3. Admin2s are created from models: djadmin2.models.register(Poll)
4. Admin2s contain methods/properties necessaey for UI
5. Views

UI Goals
---------

1. Replicate the old admin UI as closely as possible in the bootstrap/ theme. This helps us ensure that admin2/ functionality has parity with admin/.

2. Once (1) is complete and we have a stable underlying API, experiment with more interesting UI variations.
