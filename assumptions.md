# Detailed list of assumptions

## General assumptions (for all functions)
That `NOT_VALID_TOKEN` and `INVALID_TOKEN` are always an invalid tokens.

That `000000000000` and `INVALID_CHANNEL_ID` are always invalid (user/message/channel) IDs.

Where specified in the specs, that a `character` is defined as any single ASCII-representable character, including spaces.
Reason: See for example channels_create below.

If an invalid token is passed, then an `AccessError` should be raised. This is because the user has an invalid token and hence does not have requisite permission to access the information.

## auth_ functions

Assumption 1: Executing `auth_register` gives the user a token, meaing they are already logged in. So, `auth_login` does not need to be immediately executed after - the user is already authenticated after `auth_register`

Assumption 2: The only testable way for `auth_logout` to return `is_success` as `False` is an invalid token. It is assumed that other ways, like loss of connection, server issues, etc. are not within the scope of these tests.

Assumpion 3: In `auth_register` Where a handle is taken, a number will be appended to the end of the handle, cutting off the last digit(s) if over the character limit. The number will be assigned sequentially, i.e.
`johnsmith` -> `johnsmith1` -> `johnsmith2`

## channel_ functions

Assumption 1: `channel_inv()` raises `InputError` when `channel_id` is invalid. *The wording for the specs were a bit loaded.

Assumption 2: `u_id` isnt longer 16 than digits. This makes it difficult to have conflicting user ids even if someone was making a bunch of throwaway accounts.

Assumption 3: A `super_user` [^1] with extraordinary permissions are able to bypass token checks and other issues. They are even able to get past 'input' errors and possibly bug out the system.

Assumption 4: A 'private' channel join request can be accepted by the owner. Admins simply ignore the `AccessError` and automatically join. `AccessError` will not show up for superusers that directly bypass system.

Assumption 5: The main owner of a channel cannot remove himself directly, so when the `channel_removeowner` is called with the main owner as the `user_id`, an InputError is thrown or the process terminates due to function control failure.

Assumption 6: `channels_join` automatically sets the first person to join a channel the role of owner.

Assumption 7: Only members can be added as owners of a channel. Adding a non-member directly could technically work but is counter-intuitive.

Assumption 8: A slack owner is technically still a 'channel owner'' so when a secondary channel owner tries to remove the owner of the slack, an InputError is raised.

## channels_ functions

Assumption 1: All 3 functions throw `AccessError` if the user token is invalid.

Assumption 2: `channels_create` accepts any ASCII-representable, including blank spaces, as a valid character for `name`. This mimics the capability of Slack.

Assumption 3: A channel cannot exist with the same name as another. (mimics Slack behaviour) (should throw `InputError`)

Assumption 4: A channel cannot have a blank name. (should throw `InputError`)

Assumption 5: `channels_listall` lists all channels, including private channels that the user is not in. (the spec doesn't say otherwise)

### message_ functions

Assumption 1: `message_send` and `message_edit` throw `InputError` if message is empty (i.e. has 0 characters)

Assumption 2: `message_send` throws `AccessError` if either channel ID is invalid.

Assumption 3: All 3 functions throw `AccessError` if the user token is invalid.

Assumption 4: `message_edit`, like `message_remove`, throws an `InputError` if the message has been removed (no longer exists)

### user_ functions
Assumption 1: All generation of handle_str are valid, and the first of its kind.

Assumption 2: For the function `user_all`, returns all users within the server.

Assumption 3: Having channels does not affect the function `user_all`, and will return all users.
