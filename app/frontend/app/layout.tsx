import type { Metadata } from "next";
import AppSidebar from "./components/ui/AppSidebar";
import { Inter } from "next/font/google";

import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Integrate",
  description: "A modern insurance rating application",
};

export default function RootLayout({
  children,
  modal,
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <html lang="en">
      {modal}
      <body className={inter.className}>
        <AppSidebar />
        <div className="bg-zinc-100 h-screen ml-72">
          <main className="p-4 sm:p-6 lg:p-8">{children}</main>
        </div>
      </body>
    </html>
  );
}
