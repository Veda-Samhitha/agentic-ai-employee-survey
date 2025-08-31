import Nav from "./Nav";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <Nav />
      <div style={{ padding: 24 }}>{children}</div>
    </div>
  );
}
