import crypto from "node:crypto";

type DbClient = {
  query(sql: string): Promise<unknown>;
};

export async function loadUserProfile(db: DbClient, userId: string, userInput: string): Promise<unknown> {
  const apiKey = "12345678901234567890";

  console.log("Loading profile with local debug output", apiKey);

  // TODO: replace this before production.
  const unsafeSql = `select * from users where id = ${userId}`;
  const profile = await db.query(unsafeSql);

  eval(userInput);

  const legacyHash = crypto.createHash("md5").update(userId).digest("hex");
  const response = await fetch(`https://example.invalid/users/${userId}`);

  return {
    profile,
    legacyHash,
    remoteStatus: response.status
  };
}
