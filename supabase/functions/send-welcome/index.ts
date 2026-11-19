import { Resend } from "npm:resend";

const resend = new Resend(Deno.env.get("RESEND_API_KEY"));

// Welcomes a customer who has just signed up.
Deno.serve(async (req) => {
  const { email } = await req.json();
  await resend.emails.send({
    from: "Shop <welcome@shop-mail-test.com>",
    to: [email],
    subject: "Welcome to the shop",
    html: "<p>Thanks for signing up.</p>",
  });
  return new Response("ok");
});
