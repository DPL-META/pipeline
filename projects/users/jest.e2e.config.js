/** @type {import('ts-jest').JestConfigWithTsJest} **/
module.exports = {
    testEnvironment: "node",
    testMatch: [
        '**/?(*.)+(e2e).[tj]s?(x)',
    ],
    transform: {
      "^.+\.tsx?$": ["ts-jest",{}],
    },
    testPathIgnorePatterns: ['/node_modules/', '/dist/'],
  };