# Amazon Cognito

## General Info

Cognito is an identity management and sync service. There are two product streams

* Cognito Identity: handles web identity within AWS services 
* Cognito Sync: handles user application state synchronization across devices

Cognito introduces the concept of an **identity pool** which is a collection of identities

* allows grouping of identities from different providers (Google, Facebook, ...) as a single entity (kind of merged)
* this allows to login with any of them to access the same user, data and permission state
* allows identities to persist across devices
* allows two roles to be associated, one for users authenticated by a public Identity provider such as Facebook, Google, ... and a second role that can provide permissions for un-authenticated users (guests)

**=> Cognito adds the ability to authenticate as an authenticated user or a guest user.**

Cognito can orchestrate the generation of an unauthenticated identity. Cognito can merge that identity into an authenticated identity if both are provided.

The user can then use Guest login first and promote this to an authenticated identity.

The user can then login with additional identity providers which can all be merged together within Cognito.

**=> when the ID's are merged, any synced data is also merged.**

Cognito for authorization + custom built OpenID connect-compatible solution for authentication => works with identity pools