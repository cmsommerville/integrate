import { z } from "zod";

const REQUIRED_PASSWORD_LENGTH = 8;
const SPECIAL_CHARACTERS = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
const NUMBERS = /[\d]/;
const LOWERCASE = /[a-z]/;
const UPPERCASE = /[A-Z]/;

export const AuthResetPasswordInputForm = z
  .object({
    user_name: z.string(),
    old_password: z.string(),
    new_password: z.string().superRefine((val, ctx) => {
      if (val.length < REQUIRED_PASSWORD_LENGTH) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: `Password must be at least ${REQUIRED_PASSWORD_LENGTH} characters long`,
          fatal: true,
        });
        return z.NEVER;
      }

      if (!SPECIAL_CHARACTERS.test(val)) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message:
            "Password must contain at least one uppercase, one lowercase, one number, and one special character",
          fatal: true,
        });
        return z.NEVER;
      }

      if (!UPPERCASE.test(val)) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message:
            "Password must contain at least one uppercase, one lowercase, one number, and one special character",
          fatal: true,
        });
        return z.NEVER;
      }

      if (!LOWERCASE.test(val)) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message:
            "Password must contain at least one uppercase, one lowercase, one number, and one special character",
          fatal: true,
        });
        return z.NEVER;
      }

      if (!NUMBERS.test(val)) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message:
            "Password must contain at least one uppercase, one lowercase, one number, and one special character",
          fatal: true,
        });
        return z.NEVER;
      }
    }),
    confirm_password: z.string(),
  })
  .refine((data) => data.new_password === data.confirm_password, {
    message: "Passwords don't match",
    path: ["confirm_password"],
  });

export const AuthResetPasswordResponse = z.object({
  status: z.literal("success"),
  msg: z.string().optional(),
});
